# order_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from decimal import Decimal
from ..utils.auth import get_current_user
from ..models.address import Address
from ..models.product import Product
from ..models.order import Order, OrderItem
import json
import uuid


def parse_positive_int(value):
    if isinstance(value, bool):
        return None

    if isinstance(value, float):
        return None

    try:
        value = int(value)
    except (TypeError, ValueError):
        return None

    if value < 1:
        return None

    return value


@csrf_exempt
def order_list_create(request):
    # identify current user
    user = get_current_user(request)

    if not user:
        return JsonResponse({"ok": False, "message": "Unauthorized"}, status=401)

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

        return JsonResponse({
            "ok": True,
            "orders": order_list
        })

    # create new order
    if request.method == "POST":
        # parse request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "message": "Invalid JSON"}, status=400)

        address_id = parse_positive_int(data.get("address_id"))
        items = data.get("items")

        # basic validation
        if address_id is None:
            return JsonResponse({"ok": False, "message": "Invalid address_id"}, status=400)

        if not isinstance(items, list) or not items:
            return JsonResponse(
                {"ok": False, "message": "Cart items must be a non-empty list"},
                status=400
            )

        # get user's address
        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            return JsonResponse({"ok": False, "message": "Address not found"}, status=404)

        # run order creation in single transaction
        with transaction.atomic():
            subtotal = Decimal("0.00")
            shipping_fee = Decimal("0.00")
            discount = Decimal("0.00")

            order_items_data = []
            seen_product_ids = set()

            # validate products and calculate subtotal
            for item in items:
                if not isinstance(item, dict):
                    return JsonResponse(
                        {"ok": False, "message": "Each cart item must be an object"},
                        status=400
                    )

                product_id = parse_positive_int(item.get("product_id"))
                quantity = parse_positive_int(item.get("quantity"))

                if product_id is None:
                    return JsonResponse({"ok": False, "message": "Invalid product_id"}, status=400)

                if quantity is None:
                    return JsonResponse(
                        {"ok": False, "message": "Quantity must be a positive integer"},
                        status=400
                    )

                if product_id in seen_product_ids:
                    return JsonResponse(
                        {"ok": False, "message": "Duplicate product in cart items"},
                        status=400
                    )

                seen_product_ids.add(product_id)

                try:
                    product = Product.objects.select_for_update().get(
                        id=product_id,
                        is_active=True
                    )
                except Product.DoesNotExist:
                    return JsonResponse(
                        {"ok": False, "message": f"Product {product_id} not found"},
                        status=404
                    )

                if product.stock < quantity:
                    return JsonResponse({
                        "ok": False,
                        "message": f"Not enough stock for {product.title}"
                    }, status=400)

                unit_price = product.final_price
                line_total = unit_price * quantity
                subtotal += line_total

                first_image = product.images.order_by("id").first()
                image_url_snapshot = first_image.image.url if first_image and first_image.image else ""

                order_items_data.append({
                    "product": product,
                    "title_snapshot": product.title,
                    "unit_price_snapshot": unit_price,
                    "image_url_snapshot": image_url_snapshot,
                    "quantity": quantity,
                    "line_total": line_total,
                })

            if subtotal >= Decimal("50.00"):
                shipping_fee = Decimal("0.00")
            else:
                shipping_fee = Decimal("7.00")

            total = subtotal + shipping_fee - discount

            order_number = f"PP-{uuid.uuid4().hex[:12].upper()}"

            shipping_snapshot = {
                "recipient": address.recipient,
                "phone": address.phone,
                "zip": address.zip,
                "addr1": address.addr1,
                "addr2": address.addr2,
            }

            order = Order.objects.create(
                user=user,
                order_number=order_number,
                status="paid", # pending paid shipped canceled refunded
                subtotal=subtotal,
                shipping_fee=shipping_fee,
                discount=discount,
                total=total,
                shipping_snapshot=shipping_snapshot,
            )

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

    return JsonResponse({"ok": False, "message": "Method not allowed"}, status=405)