import json
from unittest.mock import patch

from django.test import TestCase, RequestFactory

from shop.models.order import Order, OrderItem
from shop.models.review import Review
from shop.views.review_views import (
    create_review,
    get_reviews,
    get_my_reviews,
    delete_my_review,
    update_my_review,
)
from shop.tests.test_helpers import create_user, create_product


class ReviewViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def create_paid_order_item(self, user, product, quantity=1):
        order = Order.objects.create(
            user=user,
            order_number="PP-REVIEW-ORDER",
            status="paid",
            subtotal=product.final_price * quantity,
            shipping_fee=0,
            discount=0,
            total=product.final_price * quantity,
            shipping_snapshot={
                "recipient": user.name,
                "phone": user.phone or "01000000000",
                "zip": "12345",
                "addr1": "Test Addr1",
                "addr2": "Test Addr2",
            },
        )

        return OrderItem.objects.create(
            order=order,
            product=product,
            title_snapshot=product.title,
            unit_price_snapshot=product.final_price,
            image_url_snapshot="",
            quantity=quantity,
            line_total=product.final_price * quantity,
        )

    # -------------------------
    # create review - auth
    # -------------------------
    @patch("shop.views.review_views.get_current_user")
    def test_create_review_requires_login(self, mock_get_current_user):
        product = create_product()
        mock_get_current_user.return_value = None

        payload = {
            "rating": 5,
            "content": "Great product",
        }

        request = self.factory.post(
            f"/api/reviews/products/{product.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = create_review(request, product.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Unauthorized")

    # -------------------------
    # create review - method / json / field validation
    # -------------------------
    @patch("shop.views.review_views.get_current_user")
    def test_create_review_get_returns_405(self, mock_get_current_user):
        user = create_user()
        product = create_product()
        mock_get_current_user.return_value = user

        request = self.factory.get(f"/api/reviews/products/{product.id}/")
        response = create_review(request, product.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Method not allowed")

    @patch("shop.views.review_views.get_current_user")
    def test_create_review_invalid_json_returns_400(self, mock_get_current_user):
        user = create_user()
        product = create_product()
        mock_get_current_user.return_value = user

        request = self.factory.post(
            f"/api/reviews/products/{product.id}/",
            data='{"rating": 5, "content": ',
            content_type="application/json",
        )

        response = create_review(request, product.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Invalid JSON")

    @patch("shop.views.review_views.get_current_user")
    def test_create_review_invalid_rating_returns_400(self, mock_get_current_user):
        user = create_user()
        product = create_product()
        mock_get_current_user.return_value = user

        payload = {
            "rating": 6,
            "content": "Great product",
        }

        request = self.factory.post(
            f"/api/reviews/products/{product.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = create_review(request, product.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Rating must be an integer between 1 and 5")

    @patch("shop.views.review_views.get_current_user")
    def test_create_review_empty_content_returns_400(self, mock_get_current_user):
        user = create_user()
        product = create_product()
        mock_get_current_user.return_value = user

        payload = {
            "rating": 5,
            "content": "",
        }

        request = self.factory.post(
            f"/api/reviews/products/{product.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = create_review(request, product.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Content is required")

    # -------------------------
    # create review - product / purchase / duplicate validation
    # -------------------------
    @patch("shop.views.review_views.get_current_user")
    def test_create_review_product_not_found_returns_404(self, mock_get_current_user):
        user = create_user()
        mock_get_current_user.return_value = user

        payload = {
            "rating": 5,
            "content": "Great product",
        }

        request = self.factory.post(
            "/api/reviews/products/9999/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = create_review(request, 9999)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Product not found")

    @patch("shop.views.review_views.get_current_user")
    def test_create_review_requires_purchase_history(self, mock_get_current_user):
        user = create_user()
        product = create_product()
        mock_get_current_user.return_value = user

        payload = {
            "rating": 5,
            "content": "Great product",
        }

        request = self.factory.post(
            f"/api/reviews/products/{product.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = create_review(request, product.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "You can only review purchased products")

    @patch("shop.views.review_views.get_current_user")
    def test_create_review_duplicate_review_returns_400(self, mock_get_current_user):
        user = create_user()
        product = create_product()
        self.create_paid_order_item(user=user, product=product)
        Review.objects.create(
            user=user,
            product=product,
            rating=5,
            content="Already reviewed",
        )
        mock_get_current_user.return_value = user

        payload = {
            "rating": 4,
            "content": "Second review",
        }

        request = self.factory.post(
            f"/api/reviews/products/{product.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = create_review(request, product.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "You already reviewed this product")

    # -------------------------
    # create review - success
    # -------------------------
    @patch("shop.views.review_views.get_current_user")
    def test_create_review_success_updates_product_rating(self, mock_get_current_user):
        user = create_user()
        product = create_product()
        self.create_paid_order_item(user=user, product=product)
        mock_get_current_user.return_value = user

        payload = {
            "rating": 5,
            "content": "Great product",
        }

        request = self.factory.post(
            f"/api/reviews/products/{product.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = create_review(request, product.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data["ok"])
        self.assertEqual(data["message"], "Review created successfully")
        self.assertEqual(Review.objects.count(), 1)

        review = Review.objects.get(user=user, product=product)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.content, "Great product")

        product.refresh_from_db()
        self.assertEqual(product.review_count, 1)
        self.assertEqual(product.avg_rating, 5.0)

    # -------------------------
    # get reviews - method / product validation
    # -------------------------
    def test_get_reviews_post_returns_405(self):
        product = create_product()

        request = self.factory.post(f"/api/reviews/products/{product.id}/list/")
        response = get_reviews(request, product.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Method not allowed")

    def test_get_reviews_product_not_found_returns_404(self):
        request = self.factory.get("/api/reviews/products/9999/list/")
        response = get_reviews(request, 9999)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Product not found")

    # -------------------------
    # get reviews - success
    # -------------------------
    def test_get_reviews_success_returns_review_list_and_rating_summary(self):
        user1 = create_user(email="user1@example.com", name="User One")
        user2 = create_user(email="user2@example.com", name="User Two")
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

        request = self.factory.get(f"/api/reviews/products/{product.id}/list/")
        response = get_reviews(request, product.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["ok"])
        self.assertEqual(data["product_id"], product.id)
        self.assertEqual(data["review_count"], 2)
        self.assertEqual(data["avg_rating"], 4.0)
        self.assertEqual(len(data["reviews"]), 2)

    # -------------------------
    # get my reviews - auth / method
    # -------------------------
    @patch("shop.views.review_views.get_current_user")
    def test_get_my_reviews_requires_login(self, mock_get_current_user):
        mock_get_current_user.return_value = None

        request = self.factory.get("/api/reviews/me/")
        response = get_my_reviews(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Unauthorized")

    @patch("shop.views.review_views.get_current_user")
    def test_get_my_reviews_post_returns_405(self, mock_get_current_user):
        user = create_user()
        mock_get_current_user.return_value = user

        request = self.factory.post("/api/reviews/me/")
        response = get_my_reviews(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Method not allowed")

    # -------------------------
    # get my reviews - success
    # -------------------------
    @patch("shop.views.review_views.get_current_user")
    def test_get_my_reviews_returns_only_my_reviews(self, mock_get_current_user):
        user = create_user(email="user1@example.com", name="User One")
        other_user = create_user(email="user2@example.com", name="User Two")
        product1 = create_product(title="Protein A")
        product2 = create_product(title="Protein B")

        Review.objects.create(
            user=user,
            product=product1,
            rating=5,
            content="My review",
        )
        Review.objects.create(
            user=other_user,
            product=product2,
            rating=4,
            content="Other review",
        )

        mock_get_current_user.return_value = user

        request = self.factory.get("/api/reviews/me/")
        response = get_my_reviews(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["ok"])
        self.assertEqual(len(data["reviews"]), 1)
        self.assertEqual(data["reviews"][0]["product_title"], "Protein A")
        self.assertEqual(data["reviews"][0]["content"], "My review")

    # -------------------------
    # delete my review - auth / method / not found
    # -------------------------
    @patch("shop.views.review_views.get_current_user")
    def test_delete_my_review_requires_login(self, mock_get_current_user):
        product = create_product()
        review = Review.objects.create(
            user=create_user(),
            product=product,
            rating=5,
            content="Review to delete",
        )
        mock_get_current_user.return_value = None

        request = self.factory.delete(f"/api/reviews/{review.id}/")
        response = delete_my_review(request, review.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Unauthorized")

    @patch("shop.views.review_views.get_current_user")
    def test_delete_my_review_get_returns_405(self, mock_get_current_user):
        user = create_user()
        mock_get_current_user.return_value = user

        request = self.factory.get("/api/reviews/1/")
        response = delete_my_review(request, 1)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Method not allowed")

    @patch("shop.views.review_views.get_current_user")
    def test_delete_my_review_not_found_for_other_users_review(self, mock_get_current_user):
        user = create_user(email="user1@example.com")
        other_user = create_user(email="user2@example.com")
        product = create_product()

        review = Review.objects.create(
            user=other_user,
            product=product,
            rating=5,
            content="Other user's review",
        )

        mock_get_current_user.return_value = user

        request = self.factory.delete(f"/api/reviews/{review.id}/")
        response = delete_my_review(request, review.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Review not found")

    # -------------------------
    # delete my review - success
    # -------------------------
    @patch("shop.views.review_views.get_current_user")
    def test_delete_my_review_success_updates_product_rating(self, mock_get_current_user):
        user = create_user(email="user1@example.com")
        other_user = create_user(email="user2@example.com")
        product = create_product()

        review1 = Review.objects.create(
            user=user,
            product=product,
            rating=5,
            content="My review",
        )
        Review.objects.create(
            user=other_user,
            product=product,
            rating=3,
            content="Other review",
        )

        mock_get_current_user.return_value = user

        request = self.factory.delete(f"/api/reviews/{review1.id}/")
        response = delete_my_review(request, review1.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["ok"])
        self.assertEqual(data["message"], "Review deleted successfully")
        self.assertFalse(Review.objects.filter(id=review1.id).exists())

        product.refresh_from_db()
        self.assertEqual(product.review_count, 1)
        self.assertEqual(product.avg_rating, 3.0)

    # -------------------------
    # update my review - auth / method / not found
    # -------------------------
    @patch("shop.views.review_views.get_current_user")
    def test_update_my_review_requires_login(self, mock_get_current_user):
        product = create_product()
        review = Review.objects.create(
            user=create_user(),
            product=product,
            rating=5,
            content="Old review",
        )
        mock_get_current_user.return_value = None

        payload = {
            "rating": 4,
            "content": "Updated review",
        }

        request = self.factory.put(
            f"/api/reviews/{review.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = update_my_review(request, review.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Unauthorized")

    @patch("shop.views.review_views.get_current_user")
    def test_update_my_review_get_returns_405(self, mock_get_current_user):
        user = create_user()
        mock_get_current_user.return_value = user

        request = self.factory.get("/api/reviews/1/")
        response = update_my_review(request, 1)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Method not allowed")

    @patch("shop.views.review_views.get_current_user")
    def test_update_my_review_not_found_for_other_users_review(self, mock_get_current_user):
        user = create_user(email="user1@example.com")
        other_user = create_user(email="user2@example.com")
        product = create_product()

        review = Review.objects.create(
            user=other_user,
            product=product,
            rating=5,
            content="Other user's review",
        )

        mock_get_current_user.return_value = user

        payload = {
            "rating": 4,
            "content": "Updated review",
        }

        request = self.factory.put(
            f"/api/reviews/{review.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = update_my_review(request, review.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Review not found")

    # -------------------------
    # update my review - validation
    # -------------------------
    @patch("shop.views.review_views.get_current_user")
    def test_update_my_review_invalid_json_returns_400(self, mock_get_current_user):
        user = create_user()
        product = create_product()

        review = Review.objects.create(
            user=user,
            product=product,
            rating=5,
            content="Old review",
        )

        mock_get_current_user.return_value = user

        request = self.factory.put(
            f"/api/reviews/{review.id}/",
            data='{"rating": 4, "content": ',
            content_type="application/json",
        )

        response = update_my_review(request, review.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Invalid JSON")

    @patch("shop.views.review_views.get_current_user")
    def test_update_my_review_invalid_rating_returns_400(self, mock_get_current_user):
        user = create_user()
        product = create_product()

        review = Review.objects.create(
            user=user,
            product=product,
            rating=5,
            content="Old review",
        )

        mock_get_current_user.return_value = user

        payload = {
            "rating": 0,
            "content": "Updated review",
        }

        request = self.factory.put(
            f"/api/reviews/{review.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = update_my_review(request, review.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Rating must be an integer between 1 and 5")

    @patch("shop.views.review_views.get_current_user")
    def test_update_my_review_empty_content_returns_400(self, mock_get_current_user):
        user = create_user()
        product = create_product()

        review = Review.objects.create(
            user=user,
            product=product,
            rating=5,
            content="Old review",
        )

        mock_get_current_user.return_value = user

        payload = {
            "rating": 4,
            "content": "",
        }

        request = self.factory.put(
            f"/api/reviews/{review.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = update_my_review(request, review.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Content is required")

    # -------------------------
    # update my review - success
    # -------------------------
    @patch("shop.views.review_views.get_current_user")
    def test_update_my_review_success_updates_review_and_product_rating(self, mock_get_current_user):
        user = create_user(email="user1@example.com")
        other_user = create_user(email="user2@example.com")
        product = create_product()

        review = Review.objects.create(
            user=user,
            product=product,
            rating=5,
            content="Old review",
        )
        Review.objects.create(
            user=other_user,
            product=product,
            rating=3,
            content="Other review",
        )

        mock_get_current_user.return_value = user

        payload = {
            "rating": 1,
            "content": "Updated review",
        }

        request = self.factory.put(
            f"/api/reviews/{review.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = update_my_review(request, review.id)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["ok"])
        self.assertEqual(data["message"], "Review updated successfully")

        review.refresh_from_db()
        self.assertEqual(review.rating, 1)
        self.assertEqual(review.content, "Updated review")

        product.refresh_from_db()
        self.assertEqual(product.review_count, 2)
        self.assertEqual(product.avg_rating, 2.0)