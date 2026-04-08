import json
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from ..utils.auth import (
    get_current_user,
    build_auth_response,
    set_auth_cookies,
    clear_auth_cookies,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from ..utils.validators import clean_text
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


User = get_user_model()


@csrf_exempt
def login(request):
    # allow only POST
    if request.method != "POST":
        return JsonResponse({"ok": False, "message": "POST only"}, status=405)

    # parse JSON body safely
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "message": "Invalid JSON"}, status=400)

    # get email and password
    email = clean_text(data.get("email"))
    password = clean_text(data.get("password"))

    if not email or not password:
        return JsonResponse({"ok": False, "message": "email or password required"}, status=400)

    # find user
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"ok": False, "message": "Invalid credentials"}, status=401)

    # check password
    if not user.check_password(password):
        return JsonResponse({"ok": False, "message": "Invalid credentials"}, status=401)

    return build_auth_response(user)


def me(request):
    if request.method != "GET":
        return JsonResponse({"ok": False, "message": "GET only"}, status=405)

    user = get_current_user(request)

    if not user:
        return JsonResponse({"ok": False, "message": "Not logged in"}, status=401)

    return JsonResponse({
        "ok": True,
        "email": user.email,
        "name": user.name,
        "role": user.role,
    })


@csrf_exempt
def logout(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "message": "POST only"}, status=405)

    response = JsonResponse({"ok": True})

    return clear_auth_cookies(response)


@csrf_exempt
def refresh(request):
    # allow only POST requests
    if request.method != "POST":
        return JsonResponse({"ok": False, "message": "POST only"}, status=405)

    # get refresh token from browser cookies
    refresh_token = request.COOKIES.get("refresh")

    # if no refresh token exists, user is not authenticated
    if not refresh_token:
        return JsonResponse({"ok": False, "message": "No refresh token"}, status=401)

    try:
        # validate the refresh token
        token = RefreshToken(refresh_token)

        # extract the user id from the token payload
        user_id = token["user_id"]

        # verify that the user still exists in the database
        user = User.objects.get(id=user_id)

        # generate a new access token using the refresh token
        new_access_token = str(token.access_token)

    except User.DoesNotExist:
        return JsonResponse({"ok": False, "message": "User not found"}, status=401)

    except TokenError:
        return JsonResponse({"ok": False, "message": "Invalid or expired refresh token"}, status=401)

    # create response object
    response = JsonResponse({"ok": True})

    return set_auth_cookies(response, new_access_token, access_max_age=300)


@csrf_exempt
def google_login(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "message": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "message": "Invalid JSON"}, status=400)

    credential = data.get("credential")

    if not credential:
        return JsonResponse({"ok": False, "message": "Google credential is required"}, status=400)

    if not settings.GOOGLE_CLIENT_ID:
        return JsonResponse({"ok": False, "message": "Google login is not configured"}, status=500)

    try:
        request_adapter = google_requests.Request()
        id_info = id_token.verify_oauth2_token(
            credential,
            request_adapter,
            settings.GOOGLE_CLIENT_ID,
        )
    except ValueError:
        return JsonResponse({"ok": False, "message": "Invalid Google token"}, status=401)

    email = id_info.get("email")
    google_sub = id_info.get("sub")
    email_verified = id_info.get("email_verified", False)
    name = id_info.get("name") or ""

    if not email or not google_sub:
        return JsonResponse({"ok": False, "message": "Google account information is incomplete"}, status=400)

    # find user by google_sub first
    user = User.objects.filter(google_sub=google_sub).first()

    # if not found, find user by email and connect google login method
    if not user:
        user = User.objects.filter(email=email).first()

        if user:
            if not user.google_sub:
                user.google_sub = google_sub
            user.email_verified = email_verified
            if not user.name and name:
                user.name = name
            user.save()

    # if still not found, create new user
    if not user:
        user = User.objects.create_user(
            email=email,
            password=None,
            name=name or "Google User",
            google_sub=google_sub,
            email_verified=email_verified,
        )

    return build_auth_response(user)


@csrf_exempt
def signup(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "message": "POST only"}, status=405)

    # parse JSON body safely
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "message": "Invalid JSON"}, status=400)

    # get signup data from request body
    username = clean_text(data.get("username"))
    email = clean_text(data.get("email"))
    password = clean_text(data.get("password"))
    conf_password = clean_text(data.get("conf_password"))
    phone = clean_text(data.get("phone"))

    # validate required fields
    if not username or not email or not password or not conf_password or not phone:
        return JsonResponse({"ok": False, "message": "All fields are required"}, status=400)

    # password does not match
    if password != conf_password:
        return JsonResponse({"ok": False, "message": "Passwords do not match"}, status=400)

    # avoid duplicated emails
    if User.objects.filter(email=email).exists():
        return JsonResponse({"ok": False, "message": "Email already exists"}, status=400)

    # create a new user
    try:
        user = User(
            name=username,
            email=email,
            phone=phone,
        )
        user.set_password(password)
        user.save()
    except IntegrityError:
        return JsonResponse({"ok": False, "message": "Signup failed"}, status=500)

    # return success response
    return JsonResponse({
        "ok": True,
        "message": "Signup successful"
    }, status=201)