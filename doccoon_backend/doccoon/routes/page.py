from django.urls import path

from doccoon.views.page import (
    PageDetailApiView,
    PageListCreateApiView,
)

urlpatterns = [
    path("", PageListCreateApiView.as_view()),
    path("<int:page_id>/", PageDetailApiView.as_view()),
]
