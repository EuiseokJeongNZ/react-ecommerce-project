import os
import django

# Connect Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from shop.models.product import Product, ProductImage
from django.core.files import File

# Local folder where product images are stored
base_path = r"C:\Users\dmltj.000\Desktop\react-ecommerce-project\client\public\images\products"

# Map product IDs to their image file names
image_map = {
    1: [
        "optimum-whey-protein-choco-1.png",
        "optimum-whey-protein-choco-2.png",
        "optimum-whey-protein-choco-3.png",
        "optimum-whey-protein-choco-4.png",
    ],
    2: [
        "musashi-isolate-protein-choco-1.png",
        "musashi-isolate-protein-choco-2.png",
    ],
    3: [
        "musashi-protein-bar-choco-lemon-cheesecake-1.png",
        "musashi-protein-bar-choco-lemon-cheesecake-2.png",
    ],
    4: [
        "balance-plant-protein-vanila-1.png",
        "balance-plant-protein-vanila-2.png",
    ],
    5: [
        "optinum-isolate-protein-choco-1.png",
        "optinum-isolate-protein-choco-2.png",
    ],
}

# Optional: remove existing product images before uploading new ones
ProductImage.objects.all().delete()

for product_id, filenames in image_map.items():
    product = Product.objects.get(id=product_id)

    for filename in filenames:
        file_path = os.path.join(base_path, filename)

        # Save each image under: products/{product_id}/{filename}
        s3_path = f"{product_id}/{filename}"

        with open(file_path, "rb") as f:
            product_image = ProductImage(product=product)
            product_image.image.save(s3_path, File(f), save=True)

        print(f"Uploaded {filename} to products/{product_id}/ for product {product_id}")

print("✅ All images uploaded successfully!")