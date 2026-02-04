from django.urls import path

from doccoon.views.sharing import (
    PublicSharedBookApiView,
    PublicSharedPageApiView,
)

urlpatterns = [
    path("book/<str:share_token>/", PublicSharedBookApiView.as_view()),
    path("page/<str:share_token>/", PublicSharedPageApiView.as_view()),
]
