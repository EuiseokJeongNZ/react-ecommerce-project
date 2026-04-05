import json

from unittest.mock import patch
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from shop.views.auth_views import signup, login, me
from shop.tests.test_helpers import create_user

User = get_user_model()


class AuthViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

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
        self.assertEqual(data["message"], "Email already exists")
        self.assertEqual(User.objects.filter(email="alex123@gmail.com").count(), 1)


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
        self.assertEqual(data["message"], "Invalid credentials")
        self.assertNotIn("access", response.cookies)
        self.assertNotIn("refresh", response.cookies)

    
    def test_me_without_login_returns_401(self):
        request = self.factory.get("/api/auth/me/")

        response = me(request)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
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