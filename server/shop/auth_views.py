from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import json

User = get_user_model()

def login(request):
    # only take POST request
    if request.method != "POST":
        return JsonResponse({"message":"POST only"}, status = 405)
    
    # 2. get email and password from body
    data = json.loads(request.body)
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JsonResponse({"message": "email or password required"}, status = 400)
    
    # 3. find user
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"message":"Invalid credentials"}, status = 401)
    
    # 4. check password
    if not user.check_password(password):
        return JsonResponse({"message":"Invalid credentials"}, status = 401)
    
    # 5. create token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    # 6.create response
    response = JsonResponse({"ok":True})

    # 7. save token in cookie
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