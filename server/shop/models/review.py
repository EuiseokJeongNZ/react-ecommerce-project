from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .user import User
from .product import Product


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )  # review writer

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )  # target product

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )  # rating 1~5

    content = models.TextField()  # review text
    created_at = models.DateTimeField(auto_now_add=True)  # created time
    updated_at = models.DateTimeField(auto_now=True)  # updated time

    class Meta:
        unique_together = ("user", "product")  # one review per user per product

    def __str__(self):
        return f"{self.user.email} - {self.product.title}"

    def update_product_rating(self):
        reviews = Review.objects.filter(product=self.product)  # all product reviews
        count = reviews.count()  # total reviews
        total = sum(review.rating for review in reviews)  # total rating
        avg = total / count if count > 0 else 0  # average rating

        self.product.avg_rating = avg  # update avg
        self.product.review_count = count  # update count
        self.product.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # save review first
        self.update_product_rating()  # refresh product rating

    def delete(self, *args, **kwargs):
        product = self.product  # keep product before delete
        super().delete(*args, **kwargs)  # delete review first

        reviews = Review.objects.filter(product=product)  # remaining reviews
        count = reviews.count()  # total reviews
        total = sum(review.rating for review in reviews)  # total rating
        avg = total / count if count > 0 else 0  # average rating

        product.avg_rating = avg  # update avg
        product.review_count = count  # update count
        product.save()