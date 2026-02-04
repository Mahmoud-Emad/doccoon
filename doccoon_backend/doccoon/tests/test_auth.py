from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from doccoon.models.user import User


def mock_throttle_allow(*args, **kwargs):
    """Always allow requests - bypass throttling in tests."""
    return True


class AuthenticationTests(TestCase):
    """Tests for authentication endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/auth/signup/"
        self.login_url = "/api/auth/login/"
        self.refresh_url = "/api/auth/token/refresh/"
        self.change_password_url = "/api/auth/change-password/"

        self.valid_user_data = {
            "email": "test@example.com",
            "password": "TestPass123!",
            "first_name": "Test",
            "last_name": "User",
        }

        # Patch throttling for all tests
        self.throttle_patcher = patch(
            "doccoon.api.throttling.AuthAnonThrottle.allow_request",
            mock_throttle_allow,
        )
        self.user_throttle_patcher = patch(
            "doccoon.api.throttling.AuthUserThrottle.allow_request",
            mock_throttle_allow,
        )
        self.throttle_patcher.start()
        self.user_throttle_patcher.start()

    def tearDown(self):
        self.throttle_patcher.stop()
        self.user_throttle_patcher.stop()

    def test_register_success(self):
        """Test successful user registration."""
        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_register_duplicate_email(self):
        """Test registration fails with duplicate email."""
        User.objects.create_user(
            email="test@example.com",
            password="ExistingPass123!",
        )
        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_invalid_email(self):
        """Test registration fails with invalid email."""
        data = self.valid_user_data.copy()
        data["email"] = "invalid-email"
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_password(self):
        """Test registration fails without password."""
        data = {"email": "test@example.com"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        """Test successful login returns tokens."""
        User.objects.create_user(
            email="test@example.com",
            password="TestPass123!",
        )
        response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "TestPass123!"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("results", data)
        self.assertIn("access_token", data["results"])
        self.assertIn("refresh_token", data["results"])

    def test_login_wrong_password(self):
        """Test login fails with wrong password."""
        User.objects.create_user(
            email="test@example.com",
            password="TestPass123!",
        )
        response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "WrongPass"},
        )
        # SimpleJWT returns 401 for invalid credentials
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        """Test login fails for non-existent user."""
        response = self.client.post(
            self.login_url,
            {"email": "nonexistent@example.com", "password": "TestPass123!"},
        )
        # SimpleJWT returns 401 for non-existent users
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_inactive_user(self):
        """Test login fails for inactive user."""
        user = User.objects.create_user(
            email="test@example.com",
            password="TestPass123!",
        )
        user.is_active = False
        user.save()

        response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "TestPass123!"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_success(self):
        """Test token refresh returns new access token."""
        User.objects.create_user(
            email="test@example.com",
            password="TestPass123!",
        )
        login_response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "TestPass123!"},
        )
        refresh_token = login_response.json()["results"]["refresh_token"]

        response = self.client.post(self.refresh_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json()["results"])

    def test_token_refresh_invalid_token(self):
        """Test token refresh fails with invalid token."""
        response = self.client.post(self.refresh_url, {"refresh": "invalid-token"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_success(self):
        """Test successful password change."""
        User.objects.create_user(
            email="test@example.com",
            password="OldPass123!",
        )
        login_response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "OldPass123!"},
        )
        token = login_response.json()["results"]["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.put(
            self.change_password_url,
            {"old_password": "OldPass123!", "new_password": "NewPass123!"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify new password works
        self.client.credentials()  # Clear auth
        login_response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "NewPass123!"},
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_change_password_wrong_old_password(self):
        """Test password change fails with wrong old password."""
        User.objects.create_user(
            email="test@example.com",
            password="OldPass123!",
        )
        login_response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "OldPass123!"},
        )
        token = login_response.json()["results"]["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.put(
            self.change_password_url,
            {"old_password": "WrongOldPass", "new_password": "NewPass123!"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password_same_password(self):
        """Test password change fails when new password equals old."""
        User.objects.create_user(
            email="test@example.com",
            password="SamePass123!",
        )
        login_response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "SamePass123!"},
        )
        token = login_response.json()["results"]["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.put(
            self.change_password_url,
            {"old_password": "SamePass123!", "new_password": "SamePass123!"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_unauthenticated(self):
        """Test password change requires authentication."""
        response = self.client.put(
            self.change_password_url,
            {"old_password": "OldPass123!", "new_password": "NewPass123!"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserSettingsTests(TestCase):
    """Tests for user settings auto-creation."""

    def setUp(self):
        self.client = APIClient()
        self.register_url = "/api/auth/signup/"

        # Patch throttling
        self.throttle_patcher = patch(
            "doccoon.api.throttling.AuthAnonThrottle.allow_request",
            mock_throttle_allow,
        )
        self.throttle_patcher.start()

    def tearDown(self):
        self.throttle_patcher.stop()

    def test_settings_created_on_registration(self):
        """Test that user settings are auto-created on registration."""
        from doccoon.models.settings import UserSettings

        response = self.client.post(
            self.register_url,
            {
                "email": "test@example.com",
                "password": "TestPass123!",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email="test@example.com")
        self.assertTrue(UserSettings.objects.filter(user=user).exists())
