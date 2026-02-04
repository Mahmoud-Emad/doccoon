from django.urls import path

from doccoon.views.auth import (
    ChangePasswordView,
    DeleteAccountView,
    LoginByTokenApiView,
    MyTokenRefreshView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterApiView,
)
from doccoon.views.user import UserProfileApiView

urlpatterns = [
    path("signup/", RegisterApiView.as_view()),
    path("login/", LoginByTokenApiView.as_view()),
    path("token/refresh/", MyTokenRefreshView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("delete-account/", DeleteAccountView.as_view()),
    path("profile/", UserProfileApiView.as_view()),
    path("password-reset/", PasswordResetRequestView.as_view()),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view()),
]
