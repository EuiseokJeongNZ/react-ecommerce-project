from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models.user import User
from rest_framework_simplejwt.tokens import AccessToken
import json


def get_current_user(request):
    access_token = request.COOKIES.get("access")

    if not access_token:
        return None

    try:
        token = AccessToken(access_token)
        user_id = token["user_id"]
        return User.objects.get(id=user_id)
    except Exception:
        return None


@csrf_exempt
def profile(request):

    user = get_current_user(request)

    if not user:
        return JsonResponse({"message": "Unauthorized"}, status=401)

    # GET profile
    if request.method == "GET":
        return JsonResponse({
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "phone": user.phone,
                "role": user.role,
                "created_at": user.created_at,
            }
        })

    # PUT profile
    if request.method == "PUT":

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)

        name = data.get("name")
        phone = data.get("phone")

        if not name:
            return JsonResponse({"message": "Name is required"}, status=400)

        user.name = name
        user.phone = phone
        user.save()

        return JsonResponse({
            "ok": True,
            "message": "Profile updated successfully",
            "user": {
                "email": user.email,
                "name": user.name,
                "phone": user.phone,
            }
        })

    return JsonResponse({"message": "Method not allowed"}, status=405)