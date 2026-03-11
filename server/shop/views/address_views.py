from django.http import JsonResponse
from ..models.address import Address
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

    except:
        return None
    
def address_list(request):
    if request.method != "GET":
        return JsonResponse({"message": "GET only"}, status=405)

    user = get_current_user(request)

    if not user:
        return JsonResponse({"message": "Unauthorized"}, status=401)

    addresses = list(
        Address.objects.filter(user=user).values(
            "id",
            "recipient",
            "phone",
            "zip",
            "addr1",
            "addr2",
            "is_default",
            "created_at",
        )
    )

    return JsonResponse({"addresses": addresses})