from django.http import JsonResponse
from .models import Product

def health(request):
    return JsonResponse({"ok": True})
    
def product_list(request):
    products = list(Product.objects.values(
        "id",
        "title",
        "tag",
        "tagline",
        "final_price",
        "original_price",
        "category",
        "info",
        "rate_count",
        "is_active",
    ))
    return JsonResponse({"products": products})