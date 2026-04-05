from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from shop.utils.auth import get_current_user
from shop.tests.test_helpers import create_user


User = get_user_model()


class AuthUtilsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    # -------------------------
    # get_current_user - no cookie
    # -------------------------
    def test_get_current_user_returns_none_when_access_cookie_missing(self):
        request = self.factory.get("/api/auth/me/")

        user = get_current_user(request)

        self.assertIsNone(user)

    # -------------------------
    # get_current_user - invalid token
    # -------------------------
    def test_get_current_user_returns_none_for_invalid_access_token(self):
        request = self.factory.get("/api/auth/me/")
        request.COOKIES["access"] = "invalid-token"

        user = get_current_user(request)

        self.assertIsNone(user)

    # -------------------------
    # get_current_user - deleted user
    # -------------------------
    def test_get_current_user_returns_none_when_user_from_token_does_not_exist(self):
        user = create_user(
            email="alex123@gmail.com",
            password="password1",
            name="Alex",
            phone="0271231234",
        )

        access_token = str(RefreshToken.for_user(user).access_token)
        user.delete()

        request = self.factory.get("/api/auth/me/")
        request.COOKIES["access"] = access_token

        result = get_current_user(request)

        self.assertIsNone(result)

    # -------------------------
    # get_current_user - success
    # -------------------------
    def test_get_current_user_returns_user_for_valid_access_token(self):
        user = create_user(
            email="alex123@gmail.com",
            password="password1",
            name="Alex",
            phone="0271231234",
        )

        access_token = str(RefreshToken.for_user(user).access_token)

        request = self.factory.get("/api/auth/me/")
        request.COOKIES["access"] = access_token

        result = get_current_user(request)

        self.assertIsNotNone(result)
        self.assertEqual(result.id, user.id)
        self.assertEqual(result.email, "alex123@gmail.com")
        self.assertEqual(result.name, "Alex")