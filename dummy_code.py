# shop/auth_views.py

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import json

User = get_user_model()


def login(request):
    # 1. POST 요청만 받기
    if request.method != "POST":
        return JsonResponse({"message": "POST only"}, status=405)

    # 2. body에서 email, password 꺼내기
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JsonResponse({"message": "email and password required"}, status=400)

    # 3. 유저 찾기
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"message": "Invalid credentials"}, status=401)

    # 4. 비밀번호 확인
    if not user.check_password(password):
        return JsonResponse({"message": "Invalid credentials"}, status=401)

    # 5. 토큰 생성
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # 6. 응답 만들기
    response = JsonResponse({"ok": True})

    # 7. 쿠키에 토큰 저장
    response.set_cookie(
        key="access",
        value=access_token,
        httponly=True,
        samesite="Lax",
    )

    response.set_cookie(
        key="refresh",
        value=refresh_token,
        httponly=True,
        samesite="Lax",
    )

    return response