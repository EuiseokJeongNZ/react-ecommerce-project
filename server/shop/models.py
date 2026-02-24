from django.db import models


class Product(models.Model):

    TAG_CHOICES = (
        ("hero-product", "Hero Product"),
        ("featured-product", "Featured Product"),
        ("normal", "Normal Product"),
    )

    tag = models.CharField(
        max_length=20,
        choices=TAG_CHOICES,
        default="normal"
    )

    tagline = models.CharField(max_length=255, blank=True)

    brand = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=255)
    info = models.TextField(blank=True)

    category = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100, blank=True)

    weight = models.CharField(max_length=100, blank=True)
    serve = models.CharField(max_length=100, blank=True)

    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    stock = models.IntegerField(default=0)

    ratings = models.IntegerField(default=0)
    rate_count = models.FloatField(default=5.0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"{self.product.title} Image"