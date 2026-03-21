from django.http import JsonResponse
from ..models.product import Product


# Simple health check endpoint (used to verify server is running)
def health(request):
    return JsonResponse({"ok": True})


# API endpoint to return all products with related images
def product_list(request):
    # Fetch all products and prefetch related images to optimize queries
    products = Product.objects.prefetch_related("images").all()

    data = []
    for product in products:
        # Convert each product into a JSON-serializable dictionary
        data.append({
            "id": product.id,
            "title": product.title,
            "tag": product.tag,
            "tagline": product.tagline,
            "final_price": str(product.final_price),  # Convert Decimal to string
            "original_price": str(product.original_price) if product.original_price else None,
            "brand": product.brand,
            "ratings": product.ratings,
            "flavor": product.flavor,
            "category": product.category,
            "info": product.info,
            "rate_count": product.rate_count,
            "is_active": product.is_active,
            # Get all image URLs for this product
            "images": [img.image.url for img in product.images.all()],
        })

    # Return product list as JSON response
    return JsonResponse({"products": data})