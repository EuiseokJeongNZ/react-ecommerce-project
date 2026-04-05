from django.test import TestCase

from shop.models.review import Review
from shop.tests.test_helpers import create_user, create_product


class ReviewModelTests(TestCase):
    # -------------------------
    # save - first review
    # -------------------------
    def test_review_save_updates_product_rating_for_first_review(self):
        user = create_user(email="user1@example.com")
        product = create_product()

        Review.objects.create(
            user=user,
            product=product,
            rating=5,
            content="Excellent product",
        )

        product.refresh_from_db()
        self.assertEqual(product.review_count, 1)
        self.assertEqual(product.avg_rating, 5.0)

    # -------------------------
    # save - multiple reviews
    # -------------------------
    def test_review_save_updates_average_rating_for_multiple_reviews(self):
        user1 = create_user(email="user1@example.com")
        user2 = create_user(email="user2@example.com")
        product = create_product()

        Review.objects.create(
            user=user1,
            product=product,
            rating=5,
            content="Excellent",
        )
        Review.objects.create(
            user=user2,
            product=product,
            rating=3,
            content="Average",
        )

        product.refresh_from_db()
        self.assertEqual(product.review_count, 2)
        self.assertEqual(product.avg_rating, 4.0)

    # -------------------------
    # save - update existing review
    # -------------------------
    def test_review_save_recalculates_rating_when_review_is_updated(self):
        user1 = create_user(email="user1@example.com")
        user2 = create_user(email="user2@example.com")
        product = create_product()

        review1 = Review.objects.create(
            user=user1,
            product=product,
            rating=5,
            content="Excellent",
        )
        Review.objects.create(
            user=user2,
            product=product,
            rating=3,
            content="Average",
        )

        product.refresh_from_db()
        self.assertEqual(product.review_count, 2)
        self.assertEqual(product.avg_rating, 4.0)

        review1.rating = 1
        review1.content = "Changed my mind"
        review1.save()

        product.refresh_from_db()
        self.assertEqual(product.review_count, 2)
        self.assertEqual(product.avg_rating, 2.0)

    # -------------------------
    # delete - one of multiple reviews
    # -------------------------
    def test_review_delete_recalculates_rating_after_deleting_one_review(self):
        user1 = create_user(email="user1@example.com")
        user2 = create_user(email="user2@example.com")
        product = create_product()

        review1 = Review.objects.create(
            user=user1,
            product=product,
            rating=5,
            content="Excellent",
        )
        Review.objects.create(
            user=user2,
            product=product,
            rating=3,
            content="Average",
        )

        product.refresh_from_db()
        self.assertEqual(product.review_count, 2)
        self.assertEqual(product.avg_rating, 4.0)

        review1.delete()

        product.refresh_from_db()
        self.assertEqual(product.review_count, 1)
        self.assertEqual(product.avg_rating, 3.0)

    # -------------------------
    # delete - last review
    # -------------------------
    def test_review_delete_sets_rating_to_zero_when_last_review_is_deleted(self):
        user = create_user(email="user1@example.com")
        product = create_product()

        review = Review.objects.create(
            user=user,
            product=product,
            rating=4,
            content="Good product",
        )

        product.refresh_from_db()
        self.assertEqual(product.review_count, 1)
        self.assertEqual(product.avg_rating, 4.0)

        review.delete()

        product.refresh_from_db()
        self.assertEqual(product.review_count, 0)
        self.assertEqual(product.avg_rating, 0)

    # -------------------------
    # unique constraint
    # -------------------------
    def test_review_unique_together_prevents_duplicate_review_for_same_user_and_product(self):
        user = create_user(email="user1@example.com")
        product = create_product()

        Review.objects.create(
            user=user,
            product=product,
            rating=5,
            content="First review",
        )

        with self.assertRaises(Exception):
            Review.objects.create(
                user=user,
                product=product,
                rating=4,
                content="Duplicate review",
            )