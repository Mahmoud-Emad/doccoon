from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request

from doccoon.api.permissions import IsBookOwner, UserIsAuthenticated
from doccoon.api.response import CustomResponse
from doccoon.api.throttling import PageOperationThrottle
from doccoon.serializers.page import (
    CreatePageSerializer,
    PageDetailSerializer,
    UpdatePageSerializer,
)
from doccoon.services.book import get_book_by_id
from doccoon.services.page import (
    get_next_page_number,
    get_page_by_id,
    get_pages_by_book,
)

# ======================================================
# Pages: List & Create
# ======================================================


@swagger_auto_schema(tags=["Pages"])
class PageListCreateApiView(ListAPIView):
    """List all pages of a book and create a new page."""

    serializer_class = PageDetailSerializer
    permission_classes = [UserIsAuthenticated, IsBookOwner]
    throttle_classes = [PageOperationThrottle]

    def get_queryset(self):
        book_id = self.kwargs["book_id"]
        return get_pages_by_book(book_id)

    def list(self, request: Request, book_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")

        queryset = self.get_queryset()
        serializer = PageDetailSerializer(queryset, many=True)
        return CustomResponse.success(
            data=serializer.data,
            message="Pages retrieved successfully.",
        )

    def post(self, request: Request, book_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")

        serializer = CreatePageSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Invalid data",
                data=serializer.errors,
            )

        page_number = get_next_page_number(book_id)
        page = serializer.save(book=book, page_number=page_number)

        return CustomResponse.success(
            data=PageDetailSerializer(page).data,
            message="Page created successfully.",
            status_code=201,
        )


# ======================================================
# Pages: Retrieve / Update / Delete
# ======================================================


@swagger_auto_schema(tags=["Pages"])
class PageDetailApiView(GenericAPIView):
    """Retrieve, update, or delete a single page."""

    permission_classes = [UserIsAuthenticated, IsBookOwner]
    throttle_classes = [PageOperationThrottle]

    def get(self, request: Request, book_id: int, page_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")

        page = get_page_by_id(page_id)
        if not page or page.book_id != book_id:
            return CustomResponse.not_found(message="Page not found")

        return CustomResponse.success(
            data=PageDetailSerializer(page).data,
            message="Page retrieved successfully.",
        )

    def put(self, request: Request, book_id: int, page_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")

        page = get_page_by_id(page_id)
        if not page or page.book_id != book_id:
            return CustomResponse.not_found(message="Page not found")

        serializer = UpdatePageSerializer(page, data=request.data, partial=True)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Invalid data",
                data=serializer.errors,
            )
        serializer.save()

        return CustomResponse.success(
            data=PageDetailSerializer(page).data,
            message="Page updated successfully.",
        )

    def delete(self, request: Request, book_id: int, page_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")

        page = get_page_by_id(page_id)
        if not page or page.book_id != book_id:
            return CustomResponse.not_found(message="Page not found")

        page.is_deleted = True
        page.deleted_at = timezone.now()
        page.save()

        return CustomResponse.success(
            message="Page deleted successfully.",
        )
