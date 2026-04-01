# porfile_views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.auth import get_current_user
from ..utils.validators import clean_text
import json

@csrf_exempt
def profile(request):

    user = get_current_user(request)

    if not user:
        return JsonResponse({"ok": False, "message": "Unauthorized"}, status=401)

    # GET profile
    if request.method == "GET":
        return JsonResponse({
            "ok": True,
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
            return JsonResponse({"ok": False, "message": "Invalid JSON"}, status=400)

        name = clean_text(data.get("name"))
        phone = clean_text(data.get("phone"))

        if not name:
            return JsonResponse({"ok": False, "message": "Name is required"}, status=400)
        
        if not phone:
            return JsonResponse({"ok": False, "message": "Phone is required"}, status=400)

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

    return JsonResponse({"ok": False, "message": "Method not allowed"}, status=405)