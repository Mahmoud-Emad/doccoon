from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from doccoon.api.permissions import IsBookOwner, UserIsAuthenticated
from doccoon.api.response import CustomResponse
from doccoon.api.throttling import BurstAnonThrottle, SharingThrottle
from doccoon.models.book import BOOK_STATUS
from doccoon.models.notification import NOTIFICATION_TYPE
from doccoon.serializers.sharing import (
    PublicBookSerializer,
    PublicPageSerializer,
    SharedBookSerializer,
    SharedPageSerializer,
)
from doccoon.services.book import get_book_by_id
from doccoon.services.notification import create_notification
from doccoon.services.page import get_page_by_id
from doccoon.services.sharing import (
    get_or_create_book_share,
    get_or_create_page_share,
    get_shared_book_by_token,
    get_shared_page_by_token,
    revoke_book_share,
    revoke_page_share,
)

# ======================================================
# Share Book (authenticated)
# ======================================================


@swagger_auto_schema(tags=["Sharing"])
class BookShareApiView(GenericAPIView):
    """Share or revoke sharing of a book."""

    permission_classes = [UserIsAuthenticated, IsBookOwner]
    throttle_classes = [SharingThrottle]

    def post(self, request: Request, book_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")
        if book.status != BOOK_STATUS.Published:
            return CustomResponse.bad_request(
                message="Only published books can be shared. Please publish the book first."
            )

        share = get_or_create_book_share(book, request.user)
        create_notification(
            user=request.user,
            notification_type=NOTIFICATION_TYPE.BookShared,
            title="Book shared",
            message=f'Your book "{book.title}" has been shared successfully.',
            related_book=book,
        )
        return CustomResponse.success(
            data=SharedBookSerializer(share).data,
            message="Book shared successfully.",
            status_code=201,
        )

    def delete(self, request: Request, book_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")

        revoked = revoke_book_share(book, request.user)
        if not revoked:
            return CustomResponse.not_found(
                message="No active share found for this book"
            )

        return CustomResponse.success(
            message="Book share revoked successfully.",
        )


# ======================================================
# Share Page (authenticated)
# ======================================================


@swagger_auto_schema(tags=["Sharing"])
class PageShareApiView(GenericAPIView):
    """Share or revoke sharing of a single page."""

    permission_classes = [UserIsAuthenticated, IsBookOwner]
    throttle_classes = [SharingThrottle]

    def post(self, request: Request, book_id: int, page_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")

        page = get_page_by_id(page_id)
        if not page or page.book_id != book_id:
            return CustomResponse.not_found(message="Page not found")

        share = get_or_create_page_share(page, book, request.user)
        create_notification(
            user=request.user,
            notification_type=NOTIFICATION_TYPE.PageShared,
            title="Page shared",
            message=f'Page {page.page_number} of "{book.title}" has been shared successfully.',
            related_book=book,
            related_page=page,
        )
        return CustomResponse.success(
            data=SharedPageSerializer(share).data,
            message="Page shared successfully.",
            status_code=201,
        )

    def delete(self, request: Request, book_id: int, page_id: int) -> CustomResponse:
        book = get_book_by_id(book_id)
        if not book:
            return CustomResponse.not_found(message="Book not found")

        page = get_page_by_id(page_id)
        if not page or page.book_id != book_id:
            return CustomResponse.not_found(message="Page not found")

        revoked = revoke_page_share(page, request.user)
        if not revoked:
            return CustomResponse.not_found(
                message="No active share found for this page"
            )

        return CustomResponse.success(
            message="Page share revoked successfully.",
        )


# ======================================================
# Public Shared Views (no auth required)
# ======================================================


@swagger_auto_schema(tags=["Sharing"])
class PublicSharedBookApiView(GenericAPIView):
    """View a shared book publicly via share token."""

    authentication_classes = []
    permission_classes = []
    throttle_classes = [BurstAnonThrottle]

    def get(self, request: Request, share_token: str) -> CustomResponse:
        shared = get_shared_book_by_token(share_token)
        if not shared:
            return CustomResponse.not_found(
                message="Shared book not found or link has been revoked"
            )

        return CustomResponse.success(
            data=PublicBookSerializer(shared).data,
            message="Shared book retrieved successfully.",
        )


@swagger_auto_schema(tags=["Sharing"])
class PublicSharedPageApiView(GenericAPIView):
    """View a shared page publicly via share token."""

    authentication_classes = []
    permission_classes = []
    throttle_classes = [BurstAnonThrottle]

    def get(self, request: Request, share_token: str) -> CustomResponse:
        shared = get_shared_page_by_token(share_token)
        if not shared:
            return CustomResponse.not_found(
                message="Shared page not found or link has been revoked"
            )

        return CustomResponse.success(
            data=PublicPageSerializer(shared).data,
            message="Shared page retrieved successfully.",
        )
