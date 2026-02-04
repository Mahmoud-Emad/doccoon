from typing import Optional

from django.db.models import Max, QuerySet

from doccoon.models.book import DoccoonPage, doccoon


def get_pages_by_book(book_id: int) -> QuerySet:
    return DoccoonPage.objects.filter(book_id=book_id, is_deleted=False).order_by(
        "page_number"
    )


def get_page_by_id(page_id: int) -> Optional[DoccoonPage]:
    try:
        return DoccoonPage.objects.get(id=page_id, is_deleted=False)
    except DoccoonPage.DoesNotExist:
        return None


def get_next_page_number(book_id: int) -> int:
    max_page = DoccoonPage.objects.filter(book_id=book_id, is_deleted=False).aggregate(
        max_page=Max("page_number")
    )
    return (max_page["max_page"] or 0) + 1
