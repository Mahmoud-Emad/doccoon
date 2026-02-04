from typing import Optional

from doccoon.models.book import DoccoonPage, doccoon
from doccoon.models.sharing import SharedBook, SharedPage
from doccoon.models.user import User


def get_shared_book_by_token(share_token: str) -> Optional[SharedBook]:
    try:
        return SharedBook.objects.select_related("book", "book__author").get(
            share_token=share_token,
            is_active=True,
            is_deleted=False,
            book__is_deleted=False,
        )
    except SharedBook.DoesNotExist:
        return None


def get_shared_page_by_token(share_token: str) -> Optional[SharedPage]:
    try:
        return SharedPage.objects.select_related("page", "page__book").get(
            share_token=share_token,
            is_active=True,
            is_deleted=False,
            page__is_deleted=False,
        )
    except SharedPage.DoesNotExist:
        return None


def _capture_book_pages(book: doccoon) -> list[dict]:
    pages = DoccoonPage.objects.filter(book=book, is_deleted=False).order_by(
        "page_number"
    )
    return [{"page_number": p.page_number, "content": p.content} for p in pages]


def get_or_create_book_share(book: doccoon, user: User) -> SharedBook:
    snapshot = _capture_book_pages(book)
    share, created = SharedBook.objects.get_or_create(
        book=book,
        shared_by=user,
        defaults={"is_active": True, "pages_snapshot": snapshot},
    )
    if not created:
        share.pages_snapshot = snapshot
        if not share.is_active:
            share.is_active = True
        share.save()
    return share


def get_or_create_page_share(
    page: DoccoonPage, book: doccoon, user: User
) -> SharedPage:
    share, created = SharedPage.objects.get_or_create(
        page=page,
        shared_by=user,
        defaults={"book": book, "is_active": True, "content_snapshot": page.content},
    )
    if not created:
        share.content_snapshot = page.content
        if not share.is_active:
            share.is_active = True
        share.save()
    return share


def revoke_book_share(book: doccoon, user: User) -> bool:
    try:
        share = SharedBook.objects.get(book=book, shared_by=user, is_active=True)
        share.is_active = False
        share.save()
        return True
    except SharedBook.DoesNotExist:
        return False


def revoke_page_share(page: DoccoonPage, user: User) -> bool:
    try:
        share = SharedPage.objects.get(page=page, shared_by=user, is_active=True)
        share.is_active = False
        share.save()
        return True
    except SharedPage.DoesNotExist:
        return False
