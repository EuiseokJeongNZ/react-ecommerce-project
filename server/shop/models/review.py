from django.db import models
from .user import User
from .product import Product


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user who wrote the review
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # product being reviewed
    rating = models.PositiveSmallIntegerField()  # rating value (1~5)
    content = models.TextField()  # review text content
    created_at = models.DateTimeField(auto_now_add=True)  # created timestamp

    class Meta:
        unique_together = ("user", "product")  # one review per user per product

    def update_product_rating(self, product):
        reviews = Review.objects.filter(product=product)  # get all reviews for this product
        total = sum([review.rating for review in reviews])  # sum all ratings
        count = reviews.count()  # count reviews
        avg = total / count if count > 0 else 0  # calculate average rating

        product.avg_rating = avg  # update average rating
        product.review_count = count  # update review count
        product.save()  # save product

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # save review first
        self.update_product_rating(self.product)  # refresh product rating

    def delete(self, *args, **kwargs):
        product = self.product  # keep product before delete
        super().delete(*args, **kwargs)  # delete review first
        self.update_product_rating(product)  # refresh product rating