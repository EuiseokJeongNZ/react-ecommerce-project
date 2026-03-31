from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()


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