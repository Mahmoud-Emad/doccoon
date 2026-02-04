"""
Social authentication views for Google and GitHub OAuth.
Handles token exchange: frontend sends the OAuth provider's access token,
backend validates it and returns JWT tokens.
"""

import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from doccoon.api.response import CustomResponse
from doccoon.api.throttling import AuthAnonThrottle
from doccoon.models.user import AUTH_PROVIDER, User
from doccoon.services.settings import get_or_create_settings


class SocialAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)


def _get_or_create_social_user(
    email: str, first_name: str, last_name: str, provider: str
) -> tuple[User | None, str | None]:
    """
    Get existing user by email or create a new one for social auth.

    Args:
        email: User's email address
        first_name: User's first name
        last_name: User's last name
        provider: OAuth provider ("google" or "github")

    Returns:
        tuple: (user, error_message) - user is None if there's an error
    """
    try:
        user = User.objects.get(email=email)
        # Block OAuth login if user originally registered with email/password
        if user.auth_provider == AUTH_PROVIDER.EMAIL:
            return (
                None,
                "An account with this email already exists. Please login with your email and password.",
            )
    except User.DoesNotExist:
        user = User.objects.create(
            email=email,
            first_name=first_name or "",
            last_name=last_name or "",
            auth_provider=provider,
        )
        user.set_unusable_password()
        user.save()
        get_or_create_settings(user)
    return user, None


def _generate_jwt_response(user: User) -> dict:
    """Generate JWT token response for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "email": user.email,
        "full_name": user.full_name,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "id": user.id,
    }


class GoogleAuthApiView(GenericAPIView):
    """Exchange Google OAuth access token for JWT tokens."""

    serializer_class = SocialAuthSerializer
    throttle_classes = [AuthAnonThrottle]

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Invalid data.", error=serializer.errors
            )

        access_token = serializer.validated_data["access_token"]

        # Validate token with Google
        try:
            resp = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10,
            )
            if resp.status_code != 200:
                return CustomResponse.bad_request(
                    message="Invalid Google access token."
                )
            data = resp.json()
        except requests.RequestException:
            return CustomResponse.bad_request(
                message="Failed to validate Google token."
            )

        email = data.get("email")
        if not email:
            return CustomResponse.bad_request(
                message="Google account does not have an email."
            )

        user, error = _get_or_create_social_user(
            email=email,
            first_name=data.get("given_name", ""),
            last_name=data.get("family_name", ""),
            provider=AUTH_PROVIDER.GOOGLE,
        )

        if error:
            return CustomResponse.bad_request(message=error)

        if not user.is_active:
            return CustomResponse.unauthorized(
                message="This account has been deactivated."
            )

        return CustomResponse.success(
            data=_generate_jwt_response(user),
            message="Logged in with Google successfully.",
        )


class GitHubAuthApiView(GenericAPIView):
    """Exchange GitHub OAuth authorization code for JWT tokens."""

    serializer_class = SocialAuthSerializer
    throttle_classes = [AuthAnonThrottle]

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Invalid data.", error=serializer.errors
            )

        code = serializer.validated_data["access_token"]

        # Exchange authorization code for access token
        from django.conf import settings as django_settings

        try:
            token_resp = requests.post(
                "https://github.com/login/oauth/access_token",
                json={
                    "client_id": django_settings.GITHUB_CLIENT_ID,
                    "client_secret": django_settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                },
                headers={"Accept": "application/json"},
                timeout=10,
            )
            token_data = token_resp.json()
            access_token = token_data.get("access_token")
            if not access_token:
                return CustomResponse.bad_request(
                    message="Failed to exchange GitHub authorization code."
                )
        except requests.RequestException:
            return CustomResponse.bad_request(
                message="Failed to exchange GitHub authorization code."
            )

        # Get user info from GitHub
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }
            user_resp = requests.get(
                "https://api.github.com/user",
                headers=headers,
                timeout=10,
            )
            if user_resp.status_code != 200:
                return CustomResponse.bad_request(
                    message="Invalid GitHub access token."
                )
            user_data = user_resp.json()
        except requests.RequestException:
            return CustomResponse.bad_request(
                message="Failed to validate GitHub token."
            )

        email = user_data.get("email")

        # GitHub email might be private, fetch from emails API
        if not email:
            try:
                emails_resp = requests.get(
                    "https://api.github.com/user/emails",
                    headers=headers,
                    timeout=10,
                )
                if emails_resp.status_code == 200:
                    emails = emails_resp.json()
                    primary = next(
                        (e for e in emails if e.get("primary") and e.get("verified")),
                        None,
                    )
                    if primary:
                        email = primary["email"]
            except requests.RequestException:
                pass

        if not email:
            return CustomResponse.bad_request(
                message="Could not retrieve email from GitHub account."
            )

        name = user_data.get("name", "") or ""
        parts = name.split(" ", 1)
        first_name = parts[0] if parts else ""
        last_name = parts[1] if len(parts) > 1 else ""

        user, error = _get_or_create_social_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            provider=AUTH_PROVIDER.GITHUB,
        )

        if error:
            return CustomResponse.bad_request(message=error)

        if not user.is_active:
            return CustomResponse.unauthorized(
                message="This account has been deactivated."
            )

        return CustomResponse.success(
            data=_generate_jwt_response(user),
            message="Logged in with GitHub successfully.",
        )
