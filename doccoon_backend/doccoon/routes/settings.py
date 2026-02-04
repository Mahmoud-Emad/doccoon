from django.urls import path

from doccoon.views.settings import UserSettingsApiView

urlpatterns = [
    path("", UserSettingsApiView.as_view()),
]
