# auth.py

from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()

COOKIE_SECURE = not settings.DEBUG
COOKIE_SAMESITE = "None" if not settings.DEBUG else "Lax"


def get_current_user(request):
    access_token = request.COOKIES.get("access")

    if not access_token:
        return None

    try:
        token = AccessToken(access_token)
        user_id = token["user_id"]
    except TokenError:
        return None

    try:
        return User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist:
        return None


def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return access_token, refresh_token


def set_auth_cookies(response, access_token, refresh_token=None, access_max_age=None):
    response.set_cookie(
        key="access",
        value=access_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        path="/",
        max_age=access_max_age,
    )

    if refresh_token is not None:
        response.set_cookie(
            key="refresh",
            value=refresh_token,
            httponly=True,
            secure=COOKIE_SECURE,
            samesite=COOKIE_SAMESITE,
            path="/",
        )

    return response


def clear_auth_cookies(response):
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


def build_auth_response(user):
    access_token, refresh_token = generate_tokens_for_user(user)

    response = JsonResponse({
        "ok": True,
        "email": user.email,
        "name": user.name,
        "role": user.role,
    })

    return set_auth_cookies(response, access_token, refresh_token)