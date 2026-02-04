from django.urls import path

from doccoon.views.social_auth import GitHubAuthApiView, GoogleAuthApiView

urlpatterns = [
    path("google/", GoogleAuthApiView.as_view()),
    path("github/", GitHubAuthApiView.as_view()),
]
