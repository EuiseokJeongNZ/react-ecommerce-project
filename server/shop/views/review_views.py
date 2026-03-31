from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from ..utils.auth import get_current_user
from ..models.review import Review
from ..models.product import Product
from ..models.order import OrderItem


@csrf_exempt
def create_review(request, product_id):
    # get logged-in user
    user = get_current_user(request)

    if not user:
        return JsonResponse({"ok": False, "message": "Unauthorized"}, status=401)

    # only POST allowed
    if request.method != "POST":
        return JsonResponse({"ok": False, "message": "Method not allowed"}, status=405)

    # parse request body
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "message": "Invalid JSON"}, status=400)

    # get input values
    rating = data.get("rating")
    content = data.get("content", "").strip()

    # check required fields
    if rating is None:
        return JsonResponse({"ok": False, "message": "Rating is required"}, status=400)

    if not content:
        return JsonResponse({"ok": False, "message": "Content is required"}, status=400)

    # convert rating
    try:
        rating = int(rating)
    except (ValueError, TypeError):
        return JsonResponse({"ok": False, "message": "Rating must be a number"}, status=400)

    # check rating range
    if rating < 1 or rating > 5:
        return JsonResponse({"ok": False, "message": "Rating must be between 1 and 5"}, status=400)

    # check product exists
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"ok": False, "message": "Product not found"}, status=404)

    # check duplicate review
    already_reviewed = Review.objects.filter(user=user, product=product).exists()
    if already_reviewed:
        return JsonResponse({"ok": False, "message": "You already reviewed this product"}, status=400)

    # check purchase history
    purchased = OrderItem.objects.filter(
        order__user=user,
        order__status__in=["paid", "shipped"],
        product=product
    ).exists()

    if not purchased:
        return JsonResponse({"ok": False, "message": "You can only review purchased products"}, status=403)

    # create review
    with transaction.atomic():
        review = Review.objects.create(
            user=user,
            product=product,
            rating=rating,
            content=content
        )

    # return result
    return JsonResponse({
        "ok": True,
        "message": "Review created successfully",
        "review": {
            "id": review.id,
            "user_id": review.user.id,
            "product_id": review.product.id,
            "rating": review.rating,
            "content": review.content,
            "created_at": review.created_at,
            "updated_at": review.updated_at,
        }
    }, status=201)


def get_reviews(request, product_id):
    # only GET allowed
    if request.method != "GET":
        return JsonResponse({"ok": False, "message": "Method not allowed"}, status=405)

    # check product exists
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"ok": False, "message": "Product not found"}, status=404)

    # get review list
    reviews = Review.objects.filter(product=product).select_related("user").order_by("-created_at")

    review_list = []

    for review in reviews:
        review_list.append({
            "id": review.id,
            "user_id": review.user.id,
            "user_name": review.user.name,
            "rating": review.rating,
            "content": review.content,
            "created_at": review.created_at,
            "updated_at": review.updated_at,
        })

    # return result
    return JsonResponse({
        "ok": True,
        "product_id": product.id,
        "avg_rating": product.avg_rating,
        "review_count": product.review_count,
        "reviews": review_list,
    }, status=200)


def get_my_reviews(request):
    # only GET allowed
    if request.method != "GET":
        return JsonResponse({"ok": False, "message": "Method not allowed"}, status=405)

    # get logged-in user
    user = get_current_user(request)

    if not user:
        return JsonResponse({"ok": False, "message": "Unauthorized"}, status=401)

    # get my reviews
    reviews = (
        Review.objects
        .filter(user=user)
        .select_related("product")
        .order_by("-created_at")
    )

    review_list = []

    for review in reviews:
        first_image = review.product.images.order_by("id").first()

        review_list.append({
            "id": review.id,
            "product_id": review.product.id,
            "product_title": review.product.title,
            "product_image": first_image.image.url if first_image and first_image.image else "",
            "rating": review.rating,
            "content": review.content,
            "created_at": review.created_at,
            "updated_at": review.updated_at,
        })

    return JsonResponse({
        "ok": True,
        "reviews": review_list,
    }, status=200)


@csrf_exempt
def delete_my_review(request, review_id):
    # only DELETE allowed
    if request.method != "DELETE":
        return JsonResponse({"ok": False, "message": "Method not allowed"}, status=405)

    # get logged-in user
    user = get_current_user(request)

    if not user:
        return JsonResponse({"ok": False, "message": "Unauthorized"}, status=401)

    try:
        review = Review.objects.get(id=review_id, user=user)
    except Review.DoesNotExist:
        return JsonResponse({"ok": False, "message": "Review not found"}, status=404)

    review.delete()

    return JsonResponse({
        "ok": True,
        "message": "Review deleted successfully",
    }, status=200)

@csrf_exempt
def update_my_review(request, review_id):
    # only PUT allowed
    if request.method != "PUT":
        return JsonResponse({"ok": False, "message": "Method not allowed"}, status=405)

    # get logged-in user
    user = get_current_user(request)

    if not user:
        return JsonResponse({"ok": False, "message": "Unauthorized"}, status=401)

    try:
        review = Review.objects.get(id=review_id, user=user)
    except Review.DoesNotExist:
        return JsonResponse({"ok": False, "message": "Review not found"}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "message": "Invalid JSON"}, status=400)

    rating = data.get("rating")
    content = data.get("content", "").strip()

    if rating is None or not content:
        return JsonResponse({"ok": False, "message": "Rating and content are required"}, status=400)

    try:
        rating = int(rating)
    except ValueError:
        return JsonResponse({"ok": False, "message": "Rating must be a number"}, status=400)

    if rating < 1 or rating > 5:
        return JsonResponse({"ok": False, "message": "Rating must be between 1 and 5"}, status=400)

    review.rating = rating
    review.content = content
    review.save()

    return JsonResponse({
        "ok": True,
        "message": "Review updated successfully",
        "review": {
            "id": review.id,
            "rating": review.rating,
            "content": review.content,
            "updated_at": review.updated_at,
        }
    }, status=200)