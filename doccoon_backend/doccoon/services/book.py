from typing import Optional

from django.db.models import Prefetch, QuerySet

from doccoon.models.book import DoccoonPage, doccoon


def get_book_pages(book_id: int) -> QuerySet[DoccoonPage]:
    """Get all the pages of a book."""
    return DoccoonPage.objects.filter(book_id=book_id, is_deleted=False).order_by(
        "page_number"
    )


def get_book_by_id(book_id: int, include_pages: bool = True) -> Optional[doccoon]:
    """Get a non-deleted book by its id.

    Args:
        book_id: The book's primary key
        include_pages: Whether to prefetch pages (default True)
    """
    if book_id is None:
        return None

    try:
        queryset = doccoon.objects.select_related("author")
        if include_pages:
            # Prefetch only non-deleted pages, ordered by page_number
            queryset = queryset.prefetch_related(
                Prefetch(
                    "doccoonpage_set",
                    queryset=DoccoonPage.objects.filter(is_deleted=False).order_by(
                        "page_number"
                    ),
                )
            )
        return queryset.get(id=int(book_id), is_deleted=False)
    except doccoon.DoesNotExist:
        return None


def get_book_by_id_simple(book_id: int) -> Optional[doccoon]:
    """Get a book by id without any prefetching - for simple existence checks."""
    if book_id is None:
        return None
    try:
        return doccoon.objects.only("id", "author_id", "status", "is_deleted").get(
            id=int(book_id), is_deleted=False
        )
    except doccoon.DoesNotExist:
        return None
