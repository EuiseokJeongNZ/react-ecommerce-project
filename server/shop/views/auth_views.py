# auth_views.py
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils.auth import get_current_user
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.db import IntegrityError

User = get_user_model()
COOKIE_SECURE = not settings.DEBUG
COOKIE_SAMESITE = "None" if not settings.DEBUG else "Lax"


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
    email = data.get("email")
    password = data.get("password")

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

    # create tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # create response
    response = JsonResponse({"ok": True})

    # save access token in cookie
    response.set_cookie(
        key="access",
        value=access_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        path="/",
    )

    # save refresh token in cookie
    response.set_cookie(
        key="refresh",
        value=refresh_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        path="/",
    )

    return response


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
    # allow only POST
    if request.method != "POST":
        return JsonResponse({"ok": False, "message": "POST only"}, status=405)

    response = JsonResponse({"ok": True})

    # delete cookies
    response.delete_cookie(
        "access",
        path="/",
        samesite=COOKIE_SAMESITE,
    )

    response.delete_cookie(
        "refresh",
        path="/",
        samesite=COOKIE_SAMESITE,
    )

    return response


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

    # store the newly issued access token in an HttpOnly cookie
    response.set_cookie(
        key="access",
        value=new_access_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        path="/",
        max_age=300,
    )

    # return response to client
    return response


@csrf_exempt
def signup(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "message": "POST only"}, status=405)
    
    # parse JSON body safely
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "message": "Invalid JSON"}, status=400)
    
    # get signup datas from request body
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    conf_password = data.get("conf_password")
    phone = data.get("phone")

    # validate requires fields
    if not username or not email or not password or not conf_password or not phone:
        return JsonResponse({"ok": False, "message": "All fields are required"}, status=400)
    
    # password do not match
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
    
    # return sucess response
    return JsonResponse({
        "ok": True,
        "message": "Signup sucessful"
    }, status=201)