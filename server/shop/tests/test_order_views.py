import json
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase, RequestFactory

from shop.models.order import Order, OrderItem
from shop.views.order_views import order_list_create
from shop.tests.test_helpers import create_user, create_product, create_address


class OrderViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    # -------------------------
    # order create - auth
    # -------------------------
    @patch("shop.views.order_views.get_current_user")
    def test_order_create_requires_login(self, mock_get_current_user):
        mock_get_current_user.return_value = None

        payload = {
            "address_id": 1,
            "items": [{"product_id": 1, "quantity": 1}],
        }

        request = self.factory.post(
            "/api/orders/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = order_list_create(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Unauthorized")

    # -------------------------
    # order create - address validation
    # -------------------------
    @patch("shop.views.order_views.get_current_user")
    def test_order_create_invalid_address_id_returns_400(self, mock_get_current_user):
        user = create_user()
        mock_get_current_user.return_value = user

        payload = {
            "address_id": "abc",
            "items": [{"product_id": 1, "quantity": 1}],
        }

        request = self.factory.post(
            "/api/orders/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = order_list_create(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Invalid address_id")

    @patch("shop.views.order_views.get_current_user")
    def test_order_create_address_not_found_returns_404(self, mock_get_current_user):
        user = create_user()
        other_user = create_user(email="other@example.com")
        other_address = create_address(user=other_user)
        mock_get_current_user.return_value = user

        payload = {
            "address_id": other_address.id,
            "items": [{"product_id": 1, "quantity": 1}],
        }

        request = self.factory.post(
            "/api/orders/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = order_list_create(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Address not found")

    # -------------------------
    # order create - items validation
    # -------------------------
    @patch("shop.views.order_views.get_current_user")
    def test_order_create_empty_items_returns_400(self, mock_get_current_user):
        user = create_user()
        address = create_address(user=user)
        mock_get_current_user.return_value = user

        payload = {
            "address_id": address.id,
            "items": [],
        }

        request = self.factory.post(
            "/api/orders/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = order_list_create(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Cart items must be a non-empty list")

    @patch("shop.views.order_views.get_current_user")
    def test_order_create_duplicate_product_returns_400(self, mock_get_current_user):
        user = create_user()
        address = create_address(user=user)
        product = create_product(stock=10)
        mock_get_current_user.return_value = user

        payload = {
            "address_id": address.id,
            "items": [
                {"product_id": product.id, "quantity": 1},
                {"product_id": product.id, "quantity": 2},
            ],
        }

        request = self.factory.post(
            "/api/orders/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = order_list_create(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Duplicate product in cart items")

    @patch("shop.views.order_views.get_current_user")
    def test_order_create_invalid_quantity_returns_400(self, mock_get_current_user):
        user = create_user()
        address = create_address(user=user)
        product = create_product(stock=10)
        mock_get_current_user.return_value = user

        payload = {
            "address_id": address.id,
            "items": [{"product_id": product.id, "quantity": 0}],
        }

        request = self.factory.post(
            "/api/orders/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = order_list_create(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Quantity must be a positive integer")

    # -------------------------
    # order create - product validation
    # -------------------------
    @patch("shop.views.order_views.get_current_user")
    def test_order_create_product_not_found_returns_404(self, mock_get_current_user):
        user = create_user()
        address = create_address(user=user)
        mock_get_current_user.return_value = user

        payload = {
            "address_id": address.id,
            "items": [{"product_id": 9999, "quantity": 1}],
        }

        request = self.factory.post(
            "/api/orders/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = order_list_create(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Product 9999 not found")

    @patch("shop.views.order_views.get_current_user")
    def test_order_create_not_enough_stock_returns_400(self, mock_get_current_user):
        user = create_user()
        address = create_address(user=user)
        product = create_product(title="Whey Protein", stock=1)
        mock_get_current_user.return_value = user

        payload = {
            "address_id": address.id,
            "items": [{"product_id": product.id, "quantity": 2}],
        }

        request = self.factory.post(
            "/api/orders/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = order_list_create(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Not enough stock for Whey Protein")

    # -------------------------
    # order create - success
    # -------------------------
    @patch("shop.views.order_views.get_current_user")
    def test_order_create_success_creates_order_items_and_decreases_stock(self, mock_get_current_user):
        user = create_user()
        address = create_address(
            user=user,
            recipient="Alex",
            phone="0271231234",
            zip="12345",
            addr1="Seoul Test-ro 123",
            addr2="101-ho",
        )
        product1 = create_product(title="Protein A", final_price="20.00", stock=10)
        product2 = create_product(title="Protein B", final_price="15.00", stock=5)
        mock_get_current_user.return_value = user

        payload = {
            "address_id": address.id,
            "items": [
                {"product_id": product1.id, "quantity": 2},
                {"product_id": product2.id, "quantity": 1},
            ],
        }

        request = self.factory.post(
            "/api/orders/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = order_list_create(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data["ok"])
        self.assertEqual(data["message"], "Order created successfully")

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 2)

        order = Order.objects.first()
        self.assertEqual(order.user, user)
        self.assertEqual(order.status, "pending")
        self.assertEqual(order.subtotal, Decimal("55.00"))
        self.assertEqual(order.shipping_fee, Decimal("0.00"))
        self.assertEqual(order.discount, Decimal("0.00"))
        self.assertEqual(order.total, Decimal("55.00"))

        self.assertEqual(order.shipping_snapshot["recipient"], "Alex")
        self.assertEqual(order.shipping_snapshot["phone"], "0271231234")
        self.assertEqual(order.shipping_snapshot["zip"], "12345")
        self.assertEqual(order.shipping_snapshot["addr1"], "Seoul Test-ro 123")
        self.assertEqual(order.shipping_snapshot["addr2"], "101-ho")

        product1.refresh_from_db()
        product2.refresh_from_db()
        self.assertEqual(product1.stock, 8)
        self.assertEqual(product2.stock, 4)

    @patch("shop.views.order_views.get_current_user")
    def test_order_create_applies_shipping_fee_under_50(self, mock_get_current_user):
        user = create_user()
        address = create_address(user=user)
        product = create_product(title="Protein A", final_price="20.00", stock=10)
        mock_get_current_user.return_value = user

        payload = {
            "address_id": address.id,
            "items": [{"product_id": product.id, "quantity": 2}],
        }

        request = self.factory.post(
            "/api/orders/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = order_list_create(request)

        self.assertEqual(response.status_code, 201)

        order = Order.objects.first()
        self.assertEqual(order.subtotal, Decimal("40.00"))
        self.assertEqual(order.shipping_fee, Decimal("7.00"))
        self.assertEqual(order.total, Decimal("47.00"))

    # -------------------------
    # order list - auth
    # -------------------------
    @patch("shop.views.order_views.get_current_user")
    def test_order_list_get_requires_login(self, mock_get_current_user):
        mock_get_current_user.return_value = None

        request = self.factory.get("/api/orders/")
        response = order_list_create(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Unauthorized")

    # -------------------------
    # order list - success
    # -------------------------
    @patch("shop.views.order_views.get_current_user")
    def test_order_list_get_returns_only_current_user_orders(self, mock_get_current_user):
        user = create_user(email="user1@example.com")
        other_user = create_user(email="user2@example.com")

        order1 = Order.objects.create(
            user=user,
            order_number="PP-ORDER1",
            status="paid", # pending paid shipped canceled refunded
            subtotal=Decimal("40.00"),
            shipping_fee=Decimal("7.00"),
            discount=Decimal("0.00"),
            total=Decimal("47.00"),
            shipping_snapshot={
                "recipient": "Alex",
                "phone": "0271231234",
                "zip": "12345",
                "addr1": "Addr1",
                "addr2": "Addr2",
            },
        )

        OrderItem.objects.create(
            order=order1,
            product=None,
            title_snapshot="Protein A",
            unit_price_snapshot=Decimal("20.00"),
            image_url_snapshot="",
            quantity=2,
            line_total=Decimal("40.00"),
        )

        Order.objects.create(
            user=other_user,
            order_number="PP-ORDER2",
            status="paid", # pending paid shipped canceled refunded
            subtotal=Decimal("10.00"),
            shipping_fee=Decimal("7.00"),
            discount=Decimal("0.00"),
            total=Decimal("17.00"),
            shipping_snapshot={
                "recipient": "Other",
                "phone": "01000000000",
                "zip": "99999",
                "addr1": "Other Addr1",
                "addr2": "Other Addr2",
            },
        )

        mock_get_current_user.return_value = user

        request = self.factory.get("/api/orders/")
        response = order_list_create(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["ok"])
        self.assertEqual(len(data["orders"]), 1)
        self.assertEqual(data["orders"][0]["order_number"], "PP-ORDER1")
        self.assertEqual(len(data["orders"][0]["items"]), 1)