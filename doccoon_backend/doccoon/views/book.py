from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request

from doccoon.api.permissions import UserIsAuthenticated
from doccoon.api.response import CustomResponse
from doccoon.api.throttling import BookOperationThrottle
from doccoon.models.book import BOOK_STATUS, doccoon
from doccoon.serializers.book import (
    BookListSerializer,
    BookSerializer,
    GetBookWithPagesSerializer,
)
from doccoon.services.book import get_book_by_id
from doccoon.services.user import get_user_by_id

# ======================================================
# Books: List & Create
# ======================================================


@swagger_auto_schema(tags=["Books"])
class BookListCreateApiView(ListAPIView):
    """
    List all books for the authenticated user
    and create a new book.
    """

    serializer_class = BookListSerializer
    permission_classes = [UserIsAuthenticated]
    throttle_classes = [BookOperationThrottle]

    def get_queryset(self):
        # Use request.user directly instead of extra DB lookup
        return (
            doccoon.objects.select_related("author")
            .prefetch_related("doccoonpage_set")
            .filter(
                author_id=self.request.user.id,
                status__in=[BOOK_STATUS.Draft, BOOK_STATUS.Published],
                is_deleted=False,
            )
            .order_by("-created_at")
        )

    def post(self, request: Request) -> CustomResponse:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Invalid data",
                data=serializer.errors,
            )

        # Use request.user directly - no need for extra DB lookup
        book = serializer.save(author=request.user)

        return CustomResponse.success(
            data=BookSerializer(book).data,
            message="Book created successfully.",
            status_code=201,
        )


# ======================================================
# Books: Retrieve / Update / Delete
# ======================================================


@swagger_auto_schema(tags=["Books"])
class BookDetailApiView(GenericAPIView):
    """
    Retrieve, update, or delete a single book.
    """

    permission_classes = [UserIsAuthenticated]
    throttle_classes = [BookOperationThrottle]

    def get(self, request: Request, book_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")

        serializer = GetBookWithPagesSerializer(book)
        return CustomResponse.success(
            data=serializer.data,
            message="Book retrieved successfully.",
        )

    def put(self, request: Request, book_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")

        serializer = BookSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return CustomResponse.success(
            data=serializer.data,
            message="Book updated successfully.",
        )

    def delete(self, request: Request, book_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")

        book.status = BOOK_STATUS.Deleted
        book.deleted_at = timezone.now()
        book.save()

        return CustomResponse.success(
            message="Book deleted successfully.",
        )


# ======================================================
# Books: Publish / Unpublish
# ======================================================


@swagger_auto_schema(tags=["Books"])
class BookPublishApiView(GenericAPIView):
    """
    Toggle a book's status between Draft and Published.
    """

    permission_classes = [UserIsAuthenticated]
    throttle_classes = [BookOperationThrottle]

    def post(self, request: Request, book_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")

        if book.author_id != request.user.id:
            return CustomResponse.unauthorized(
                message="You are not the author of this book."
            )

        if book.status == BOOK_STATUS.Published:
            book.status = BOOK_STATUS.Draft
            book.save()
            return CustomResponse.success(
                data=BookSerializer(book).data,
                message="Book unpublished successfully.",
            )

        book.status = BOOK_STATUS.Published
        book.save()
        return CustomResponse.success(
            data=BookSerializer(book).data,
            message="Book published successfully.",
        )
