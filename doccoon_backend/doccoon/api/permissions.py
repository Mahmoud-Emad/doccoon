from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from doccoon.models.book import doccoon


class UserIsAuthenticated(permissions.BasePermission):
    """Logged in permission."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.user.is_authenticated and request.user.is_active


class IsBookOwner(permissions.BasePermission):
    """Verify the authenticated user owns the book referenced by book_id in the URL."""

    message = "You do not own this book"

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user.is_authenticated:
            return False

        book_id = view.kwargs.get("book_id")
        if book_id is None:
            return True

        try:
            book = doccoon.objects.get(id=book_id)
        except doccoon.DoesNotExist:
            return True  # let the view handle 404

        return book.author_id == request.user.id
