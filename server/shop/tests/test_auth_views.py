import json
from unittest.mock import patch

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from shop.views.auth_views import signup, login, logout, me, refresh
from shop.tests.test_helpers import create_user


User = get_user_model()


class AuthViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    # -------------------------
    # signup
    # -------------------------
    def test_signup_success(self):
        payload = {
            "username": "Alex",
            "email": "alex123@gmail.com",
            "password": "password1",
            "conf_password": "password1",
            "phone": "0271231234",
        }

        request = self.factory.post(
            "/api/auth/signup/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = signup(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data["ok"])
        self.assertEqual(data["message"], "Signup successful")
        self.assertTrue(User.objects.filter(email="alex123@gmail.com").exists())

        user = User.objects.get(email="alex123@gmail.com")
        self.assertEqual(user.name, "Alex")
        self.assertEqual(user.phone, "0271231234")

    def test_signup_password_mismatch(self):
        payload = {
            "username": "Alex",
            "email": "alex123@gmail.com",
            "password": "password1",
            "conf_password": "password2",
            "phone": "0271231234",
        }

        request = self.factory.post(
            "/api/auth/signup/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = signup(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Passwords do not match")
        self.assertFalse(User.objects.filter(email="alex123@gmail.com").exists())

    def test_signup_duplicate_email(self):
        create_user(
            email="alex123@gmail.com",
            password="password1",
            name="Existing User",
            phone="01011112222",
        )

        payload = {
            "username": "Alex",
            "email": "alex123@gmail.com",
            "password": "password1",
            "conf_password": "password1",
            "phone": "0271231234",
        }

        request = self.factory.post(
            "/api/auth/signup/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = signup(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Email already exists")
        self.assertEqual(User.objects.filter(email="alex123@gmail.com").count(), 1)

    def test_signup_missing_required_field(self):
        payload = {
            "username": "Alex",
            "email": "alex123@gmail.com",
            "password": "password1",
            "conf_password": "password1",
            "phone": "",
        }

        request = self.factory.post(
            "/api/auth/signup/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = signup(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "All fields are required")
        self.assertFalse(User.objects.filter(email="alex123@gmail.com").exists())

    def test_signup_invalid_json_returns_400(self):
        request = self.factory.post(
            "/api/auth/signup/",
            data='{"username": "Alex", "email": ',
            content_type="application/json",
        )

        response = signup(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Invalid JSON")

    def test_signup_get_returns_405(self):
        request = self.factory.get("/api/auth/signup/")

        response = signup(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "POST only")

    # -------------------------
    # login
    # -------------------------
    def test_login_success_sets_access_and_refresh_cookies(self):
        create_user(
            email="alex123@gmail.com",
            password="password1",
            name="Alex",
            phone="0271231234",
        )

        payload = {
            "email": "alex123@gmail.com",
            "password": "password1",
        }

        request = self.factory.post(
            "/api/auth/login/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = login(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["ok"])
        self.assertIn("access", response.cookies)
        self.assertIn("refresh", response.cookies)
        self.assertTrue(response.cookies["access"].value)
        self.assertTrue(response.cookies["refresh"].value)

    def test_login_wrong_password_returns_401(self):
        create_user(
            email="alex123@gmail.com",
            password="password1",
            name="Alex",
            phone="0271231234",
        )

        payload = {
            "email": "alex123@gmail.com",
            "password": "wrongpassword",
        }

        request = self.factory.post(
            "/api/auth/login/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = login(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Invalid credentials")
        self.assertNotIn("access", response.cookies)
        self.assertNotIn("refresh", response.cookies)

    def test_login_nonexistent_user_returns_401(self):
        payload = {
            "email": "nouser@gmail.com",
            "password": "password1",
        }

        request = self.factory.post(
            "/api/auth/login/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = login(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Invalid credentials")

    def test_login_missing_required_field_returns_400(self):
        payload = {
            "email": "alex123@gmail.com",
            "password": "",
        }

        request = self.factory.post(
            "/api/auth/login/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        response = login(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "email or password required")

    def test_login_invalid_json_returns_400(self):
        request = self.factory.post(
            "/api/auth/login/",
            data='{"email": "alex123@gmail.com", ',
            content_type="application/json",
        )

        response = login(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Invalid JSON")

    def test_login_get_returns_405(self):
        request = self.factory.get("/api/auth/login/")

        response = login(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "POST only")

    # -------------------------
    # me
    # -------------------------
    def test_me_without_login_returns_401(self):
        request = self.factory.get("/api/auth/me/")

        response = me(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Not logged in")

    @patch("shop.views.auth_views.get_current_user")
    def test_me_with_logged_in_user_returns_user_info(self, mock_get_current_user):
        user = create_user(
            email="alex123@gmail.com",
            password="password1",
            name="Alex",
            phone="0271231234",
            role="customer",
        )

        mock_get_current_user.return_value = user

        request = self.factory.get("/api/auth/me/")
        response = me(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["ok"])
        self.assertEqual(data["email"], "alex123@gmail.com")
        self.assertEqual(data["name"], "Alex")
        self.assertEqual(data["role"], "customer")

    def test_me_post_returns_405(self):
        request = self.factory.post("/api/auth/me/")

        response = me(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "GET only")

    # -------------------------
    # logout
    # -------------------------
    def test_logout_success_deletes_access_and_refresh_cookies(self):
        request = self.factory.post("/api/auth/logout/")

        response = logout(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["ok"])
        self.assertIn("access", response.cookies)
        self.assertIn("refresh", response.cookies)
        self.assertEqual(response.cookies["access"].value, "")
        self.assertEqual(response.cookies["refresh"].value, "")

    def test_logout_get_returns_405(self):
        request = self.factory.get("/api/auth/logout/")

        response = logout(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "POST only")

    # -------------------------
    # refresh
    # -------------------------
    def test_refresh_success_sets_new_access_cookie(self):
        user = create_user(
            email="alex123@gmail.com",
            password="password1",
            name="Alex",
            phone="0271231234",
        )
        refresh_token = str(RefreshToken.for_user(user))

        request = self.factory.post("/api/auth/refresh/")
        request.COOKIES["refresh"] = refresh_token

        response = refresh(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["ok"])
        self.assertIn("access", response.cookies)
        self.assertTrue(response.cookies["access"].value)

    def test_refresh_without_cookie_returns_401(self):
        request = self.factory.post("/api/auth/refresh/")

        response = refresh(request)
        data = json.loads(response.content)  # ADD THIS LINE

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "No refresh token")

    def test_refresh_with_invalid_token_returns_401(self):
        request = self.factory.post("/api/auth/refresh/")
        request.COOKIES["refresh"] = "invalid-token"

        response = refresh(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "Invalid refresh token")

    def test_refresh_get_returns_405(self):
        request = self.factory.get("/api/auth/refresh/")

        response = refresh(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data["ok"])
        self.assertEqual(data["message"], "POST only")