from django.urls import include, path

from doccoon.views.book import (
    BookDetailApiView,
    BookListCreateApiView,
    BookPublishApiView,
)
from doccoon.views.sharing import BookShareApiView, PageShareApiView

urlpatterns = [
    path("", BookListCreateApiView.as_view()),
    path("<int:book_id>/", BookDetailApiView.as_view()),
    path("<int:book_id>/publish/", BookPublishApiView.as_view()),
    path("<int:book_id>/pages/", include("doccoon.routes.page")),
    path("<int:book_id>/share/", BookShareApiView.as_view()),
    path("<int:book_id>/pages/<int:page_id>/share/", PageShareApiView.as_view()),
]
