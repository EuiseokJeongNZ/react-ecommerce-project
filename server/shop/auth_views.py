# auth_views.py

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import json
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@csrf_exempt
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

def me(request):
    access_token = request.COOKIES.get("access")

    # allow only POST requests for login
    if not access_token:
        return JsonResponse({"message":"Not logged in"}, status=401)
    
    if request.method != "GET":
        return JsonResponse({"message": "GET only"}, status=405)
    
    try:
        # decode token and extract user id
        token = AccessToken(access_token)
        user_id = token["user_id"]
        # retrieve user from database
        user = User.objects.get(id=user_id)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=401)
    
    # return logged-in user information
    return JsonResponse({
        "email":user.email,
        "name":user.name,
        "role":user.role,
    })