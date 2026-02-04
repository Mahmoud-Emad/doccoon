from typing import Optional

from django.db.models import QuerySet

from doccoon.models.book import DoccoonPage, doccoon


def get_book_pages(book_id: int) -> QuerySet[DoccoonPage]:
    """Get all the pages of a book."""
    return DoccoonPage.objects.filter(book_id=book_id, is_deleted=False).order_by(
        "page_number"
    )


def get_book_by_id(book_id: int) -> Optional[doccoon]:
    """Get a non-deleted book by its id."""
    if book_id is None:
        return None

    try:
        return (
            doccoon.objects.select_related("author")
            .prefetch_related("doccoonpage_set")
            .get(id=int(book_id), is_deleted=False)
        )
    except doccoon.DoesNotExist:
        return None
