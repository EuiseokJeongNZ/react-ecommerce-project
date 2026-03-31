from django.http import JsonResponse
from ..models.address import Address
from ..utils.auth import get_current_user
from django.views.decorators.csrf import csrf_exempt
import json

# api for getting address list or creating address
@csrf_exempt
def address_list(request):

    # get current user
    user = get_current_user(request)

    # block request if not logged in
    if not user:
        return JsonResponse({"ok": False, "message": "Unauthorized"}, status=401)

    # get address list
    if request.method == "GET":
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

        return JsonResponse({
            "ok": True,
            "addresses": addresses
        })

    # create new address
    if request.method == "POST":

        # read json body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "message": "Invalid JSON"}, status=400)

        # get data from request
        recipient = data.get("recipient")
        phone = data.get("phone")
        zip_code = data.get("zip")
        addr1 = data.get("addr1")
        addr2 = data.get("addr2", "")
        is_default = data.get("is_default", False)

        # check required fields
        if not recipient or not phone or not zip_code or not addr1:
            return JsonResponse({"ok": False, "message": "Required fields are missing"}, status=400)

        # only one default address allowed
        if is_default:
            Address.objects.filter(user=user, is_default=True).update(is_default=False)

        # create address
        address = Address.objects.create(
            user=user,
            recipient=recipient,
            phone=phone,
            zip=zip_code,
            addr1=addr1,
            addr2=addr2,
            is_default=is_default,
        )

        return JsonResponse({
            "ok": True,
            "message": "Address created successfully",
            "address": {
                "id": address.id,
                "recipient": address.recipient,
                "phone": address.phone,
                "zip": address.zip,
                "addr1": address.addr1,
                "addr2": address.addr2,
                "is_default": address.is_default,
            }
        }, status=201)

    return JsonResponse({"ok": False, "message": "Method not allowed"}, status=405)


# api for updating or deleting one address
@csrf_exempt
def address_detail(request, address_id):

    # get current user
    user = get_current_user(request)

    if not user:
        return JsonResponse({"ok": False, "message": "Unauthorized"}, status=401)

    # find address belonging to this user
    try:
        address = Address.objects.get(id=address_id, user=user)
    except Address.DoesNotExist:
        return JsonResponse({"ok": False, "message": "Address not found"}, status=404)
    
    # update address
    if request.method == "PUT":

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "message": "Invalid JSON"}, status=400)

        recipient = data.get("recipient")
        phone = data.get("phone")
        zip_code = data.get("zip")
        addr1 = data.get("addr1")
        addr2 = data.get("addr2", "")
        is_default = data.get("is_default", False)

        if not recipient or not phone or not zip_code or not addr1:
            return JsonResponse({"ok": False, "message": "Required fields are missing"}, status=400)

        # keep only one default address
        if is_default:
            Address.objects.filter(user=user, is_default=True).exclude(id=address.id).update(is_default=False)

        # update fields
        address.recipient = recipient
        address.phone = phone
        address.zip = zip_code
        address.addr1 = addr1
        address.addr2 = addr2
        address.is_default = is_default
        address.save()

        return JsonResponse({
            "ok": True,
            "message": "Address updated successfully",
            "address": {
                "id": address.id,
                "recipient": address.recipient,
                "phone": address.phone,
                "zip": address.zip,
                "addr1": address.addr1,
                "addr2": address.addr2,
                "is_default": address.is_default,
            }
        })

    # delete address
    if request.method == "DELETE":
        address.delete()

        return JsonResponse({
            "ok": True,
            "message": "Address deleted successfully"
        })

    return JsonResponse({"ok": False, "message": "Method not allowed"}, status=405)