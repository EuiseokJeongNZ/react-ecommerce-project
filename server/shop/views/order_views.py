# order_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from decimal import Decimal
from datetime import datetime
from rest_framework_simplejwt.tokens import AccessToken
from ..models.user import User
from ..models.address import Address
from ..models.product import Product
from ..models.order import Order, OrderItem
import json


# get logged-in user from jwt access token in cookie
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
def order_list_create(request):

    # identify current user
    user = get_current_user(request)

    if not user:
        return JsonResponse({"message": "Unauthorized"}, status=401)

    # get user's order list
    if request.method == "GET":
        orders = Order.objects.filter(user=user).order_by("-created_at")

        order_list = []

        for order in orders:
            items = []

            # collect order items
            for item in order.items.all():
                items.append({
                    "id": item.id,
                    "product_id": item.product.id if item.product else None,
                    "title_snapshot": item.title_snapshot,
                    "unit_price_snapshot": str(item.unit_price_snapshot),
                    "image_url_snapshot": item.image_url_snapshot,
                    "quantity": item.quantity,
                    "line_total": str(item.line_total),
                })

            # build order response
            order_list.append({
                "id": order.id,
                "order_number": order.order_number,
                "status": order.status,
                "subtotal": str(order.subtotal),
                "shipping_fee": str(order.shipping_fee),
                "discount": str(order.discount),
                "total": str(order.total),
                "shipping_snapshot": order.shipping_snapshot,
                "created_at": order.created_at,
                "items": items,
            })

        return JsonResponse({"orders": order_list})


    # create new order
    if request.method == "POST":

        # parse request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)

        address_id = data.get("address_id")
        items = data.get("items", [])

        # basic validation
        if not address_id:
            return JsonResponse({"message": "Address is required"}, status=400)

        if not items:
            return JsonResponse({"message": "Cart items are required"}, status=400)

        # get user's address
        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            return JsonResponse({"message": "Address not found"}, status=404)

        subtotal = Decimal("0.00")
        shipping_fee = Decimal("0.00")
        discount = Decimal("0.00")

        order_items_data = []

        # validate products and calculate subtotal
        for item in items:
            product_id = item.get("product_id")
            quantity = item.get("quantity")

            if not product_id or not quantity:
                return JsonResponse({"message": "Invalid item data"}, status=400)

            try:
                product = Product.objects.get(id=product_id, is_active=True)
            except Product.DoesNotExist:
                return JsonResponse({"message": f"Product {product_id} not found"}, status=404)

            # check stock
            if product.stock < quantity:
                return JsonResponse({
                    "message": f"Not enough stock for {product.title}"
                }, status=400)

            unit_price = product.final_price
            line_total = unit_price * quantity
            subtotal += line_total

            # save snapshot data for order item
            order_items_data.append({
                "product": product,
                "title_snapshot": product.title,
                "unit_price_snapshot": unit_price,
                "image_url_snapshot": "",
                "quantity": quantity,
                "line_total": line_total,
            })

        if subtotal >= Decimal("50.00"):
            shipping_fee = Decimal("0.00")
        else:
            shipping_fee = Decimal("7.00")

        # calculate order total
        total = subtotal + shipping_fee - discount

        # generate order number
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        order_number = f"PP-{now}-{user.id}"

        # snapshot shipping info
        shipping_snapshot = {
            "recipient": address.recipient,
            "phone": address.phone,
            "zip": address.zip,
            "addr1": address.addr1,
            "addr2": address.addr2,
        }

        # run order creation in single transaction
        with transaction.atomic():

            order = Order.objects.create(
                user=user,
                order_number=order_number,
                status="pending",
                subtotal=subtotal,
                shipping_fee=shipping_fee,
                discount=discount,
                total=total,
                shipping_snapshot=shipping_snapshot,
            )

            # create order items and update stock
            for item_data in order_items_data:

                OrderItem.objects.create(
                    order=order,
                    product=item_data["product"],
                    title_snapshot=item_data["title_snapshot"],
                    unit_price_snapshot=item_data["unit_price_snapshot"],
                    image_url_snapshot=item_data["image_url_snapshot"],
                    quantity=item_data["quantity"],
                    line_total=item_data["line_total"],
                )

                product = item_data["product"]
                product.stock -= item_data["quantity"]
                product.save()

        # return created order info
        return JsonResponse({
            "ok": True,
            "message": "Order created successfully",
            "order": {
                "id": order.id,
                "order_number": order.order_number,
                "status": order.status,
                "subtotal": str(order.subtotal),
                "shipping_fee": str(order.shipping_fee),
                "discount": str(order.discount),
                "total": str(order.total),
                "shipping_snapshot": order.shipping_snapshot,
                "created_at": order.created_at,
            }
        }, status=201)

    return JsonResponse({"message": "Method not allowed"}, status=405)