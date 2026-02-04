from datetime import datetime
from typing import Dict

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from doccoon.api.permissions import UserIsAuthenticated
from doccoon.api.response import CustomResponse
from doccoon.api.throttling import AuthAnonThrottle, AuthUserThrottle
from doccoon.models.user import AUTH_PROVIDER, User
from doccoon.serializers.auth import (
    ChangePasswordSerializer,
    MyTokenObtainPairSerializer,
    MyTokenRefreshSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
)
from doccoon.services.settings import get_or_create_settings
from doccoon.services.user import get_user_by_email


class RegisterApiView(GenericAPIView):
    """
    API view for registering a new user in the database.
    """

    serializer_class = RegisterSerializer
    throttle_classes = [AuthAnonThrottle]

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request: Request) -> Response:
        """
        Handle POST request to register a new user.

        Parameters:
        - request (Request): The request object containing user data.

        Returns:
        - Response: Custom response indicating success or failure.
        """

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Create the user object
            user: User = serializer.save()
            # Auto-create default settings for the new user
            get_or_create_settings(user)
            return CustomResponse.success(
                data=serializer.data,
                message="User created successfully.",
                status_code=201,
            )

        # Handle invalid serializer data
        return self._handle_serializer_errors(serializer)

    @staticmethod
    def _handle_serializer_errors(serializer: Serializer) -> Response:
        """
        Handle errors from an invalid serializer.

        Parameters:
        - serializer (Serializer): The serializer instance.

        Returns:
        - Response: Custom bad request response.
        """
        error_message = " ".join(
            f"{field}: {', '.join(errors)}"
            for field, errors in serializer.errors.items()
        )
        return CustomResponse.bad_request(
            error=serializer.errors,
            message=f"Failed to create user due to: {error_message}",
        )


class LoginByTokenApiView(TokenObtainPairView):
    """Class LoginByTokenAPIView to login a user by jwt token"""

    serializer_class = MyTokenObtainPairSerializer
    throttle_classes = [AuthAnonThrottle]

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request: Request) -> Response:
        """Method to register a new user"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data.get("email")
            user = get_user_by_email(user_email)
            if not user.is_active:
                return CustomResponse.unauthorized(
                    message="You don't have permission to perform this action."
                )
            return CustomResponse.success(
                data=serializer.custom_token(data=serializer.data),
                message="User logged in successfully",
            )
        return CustomResponse.bad_request(
            error=serializer.errors,
            message=f"Failed to login user due to: {serializer.errors}",
        )


class MyTokenRefreshView(TokenRefreshView):
    """
    An end point to refresh the user token
    """

    serializer_class = MyTokenRefreshSerializer

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request: Request) -> Response:
        """Method to refresh the user token"""
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                return CustomResponse.success(
                    data=serializer.validated_data,
                    message="User token refreshed successfully",
                )
        except Exception:
            return CustomResponse.bad_request(
                message="Invalid or expired refresh token.",
            )
        return CustomResponse.bad_request(
            error=serializer.errors,
            message=f"Failed to refresh user token due to: {serializer.errors}",
        )


class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [UserIsAuthenticated]

    @swagger_auto_schema(tags=["Auth"])
    def put(self, request: Request) -> Response:
        """Change user password. OAuth users without a password can set one without old_password."""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Please make sure that you entered valid data.",
                error=serializer.errors,
            )

        old_password: str = serializer.validated_data.get("old_password", "")
        new_password: str = serializer.validated_data.get("new_password")
        user = request.user
        has_usable_password = user.has_usable_password()

        # Validate new password
        if not new_password or len(new_password) < 8:
            return CustomResponse.bad_request(
                message="New password must be at least 8 characters."
            )

        # If user has a password, require old_password
        if has_usable_password:
            if not old_password:
                return CustomResponse.bad_request(
                    message="Current password is required."
                )

            if old_password == new_password:
                return CustomResponse.bad_request(
                    message="The new password must be different from the current password."
                )

            if not check_password(old_password, user.password):
                return CustomResponse.unauthorized(
                    message="Incorrect current password."
                )

        # Set the new password
        user.set_password(new_password)
        user.save()

        message = (
            "Password updated successfully."
            if has_usable_password
            else "Password set successfully."
        )
        return CustomResponse.success(message=message)


class DeleteAccountView(GenericAPIView):
    """API view for deleting user account."""

    permission_classes = [UserIsAuthenticated]

    @swagger_auto_schema(tags=["Auth"])
    def delete(self, request: Request) -> Response:
        """
        Delete the authenticated user's account.
        This performs a hard delete of the user and all associated data.
        """
        user = request.user

        # Delete the user (this will cascade to related objects)
        user.delete()

        return CustomResponse.success(
            message="Your account has been deleted successfully."
        )


class PasswordResetRequestView(GenericAPIView):
    """API view for requesting a password reset email."""

    serializer_class = PasswordResetRequestSerializer
    throttle_classes = [AuthAnonThrottle]

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Please provide a valid email.",
                error=serializer.errors,
            )

        email = serializer.validated_data["email"]

        # Always return success to prevent email enumeration
        success_message = (
            "If an account with this email exists, "
            "you will receive a password reset link shortly."
        )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return CustomResponse.success(message=success_message)

        # Check if user registered via OAuth
        if user.auth_provider != AUTH_PROVIDER.EMAIL:
            # Still return success to prevent enumeration, but don't send email
            # User should use their OAuth provider to login
            return CustomResponse.success(message=success_message)

        # Generate reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build reset URL (frontend URL)
        frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:5173")
        reset_url = f"{frontend_url}/reset-password?token={token}&uid={uid}"

        # Send email
        subject = "Reset your Doccoon password"
        message = f"""Hi {user.first_name},

You requested to reset your password for your Doccoon account.

Click the link below to reset your password:
{reset_url}

This link will expire in 24 hours.

If you didn't request this, you can safely ignore this email.

Best,
The Doccoon Team
"""
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception:
            return CustomResponse.bad_request(
                message="Failed to send reset email. Please try again later."
            )

        return CustomResponse.success(message=success_message)


class PasswordResetConfirmView(GenericAPIView):
    """API view for confirming password reset with token."""

    serializer_class = PasswordResetConfirmSerializer
    throttle_classes = [AuthAnonThrottle]

    @swagger_auto_schema(tags=["Auth"])
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Invalid data.",
                error=serializer.errors,
            )

        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]
        uid = request.data.get("uid", "")

        if len(new_password) < 8:
            return CustomResponse.bad_request(
                message="Password must be at least 8 characters."
            )

        # Decode user ID
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return CustomResponse.bad_request(message="Invalid or expired reset link.")

        # Verify token
        if not default_token_generator.check_token(user, token):
            return CustomResponse.bad_request(message="Invalid or expired reset link.")

        # Set new password
        user.set_password(new_password)
        user.save()

        return CustomResponse.success(
            message="Your password has been reset successfully. You can now login."
        )
