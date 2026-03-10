# auth_views.py

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.views.decorators.csrf import csrf_exempt
import json

User = get_user_model()


@csrf_exempt
def login(request):
    # allow only POST
    if request.method != "POST":
        return JsonResponse({"message": "POST only"}, status=405)

    # parse JSON body safely
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON"}, status=400)

    # get email and password
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JsonResponse({"message": "email or password required"}, status=400)

    # find user
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"message": "Invalid credentials"}, status=401)

    # check password
    if not user.check_password(password):
        return JsonResponse({"message": "Invalid credentials"}, status=401)

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
        samesite="Lax",
        path="/",
    )

    # save refresh token in cookie
    response.set_cookie(
        key="refresh",
        value=refresh_token,
        httponly=True,
        samesite="Lax",
        path="/",
    )

    return response


def me(request):
    # allow only GET
    if request.method != "GET":
        return JsonResponse({"message": "GET only"}, status=405)

    # get access token from cookie
    access_token = request.COOKIES.get("access")

    if not access_token:
        return JsonResponse({"message": "Not logged in"}, status=401)

    try:
        # decode token
        token = AccessToken(access_token)
        user_id = token["user_id"]

        # get user from DB
        user = User.objects.get(id=user_id)

    except User.DoesNotExist:
        return JsonResponse({"message": "User not found"}, status=401)

    except Exception:
        return JsonResponse({"message": "Invalid or expired token"}, status=401)

    # return current user info
    return JsonResponse({
        "email": user.email,
        "name": user.name,
        "role": user.role,
    })


@csrf_exempt
def logout(request):
    print("logout view called")
    # allow only POST
    if request.method != "POST":
        return JsonResponse({"message": "POST only"}, status=405)

    response = JsonResponse({"ok": True})

    # delete cookies
    response.delete_cookie("access", path="/")
    response.delete_cookie("refresh", path="/")

    return response

@csrf_exempt
def refresh(request):
    # allow only POST requests
    if request.method != "POST":
        return JsonResponse({"message": "POST only"}, status=405)

    # get refresh token from browser cookies
    refresh_token = request.COOKIES.get("refresh")

    # if no refresh token exists, user is not authenticated
    if not refresh_token:
        return JsonResponse({"message": "No refresh token"}, status=401)

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
        # user id in token does not exist anymore
        return JsonResponse({"message": "User not found"}, status=401)

    except Exception:
        # refresh token is invalid or expired
        return JsonResponse({"message": "Invalid or expired refresh token"}, status=401)

    # create response object
    response = JsonResponse({"ok": True})

    # store the newly issued access token in an HttpOnly cookie
    response.set_cookie(
        key="access",
        value=new_access_token,
        httponly=True,
        samesite="Lax",
        path="/",
    )

    # return response to client
    return response