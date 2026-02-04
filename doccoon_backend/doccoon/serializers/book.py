import re
from datetime import datetime

from rest_framework import serializers

from doccoon.models.book import DoccoonPage, doccoon
from doccoon.services.book import get_book_pages
from doccoon.utils.sanitize import sanitize_plain_text

IMAGE_PATTERN = re.compile(r"!\[.*?\]\(.*?\)|<img\s[^>]*>")


class PageSerializer(serializers.ModelSerializer):
    """serializer for page with content"""

    class Meta:
        model = DoccoonPage
        fields = [
            "id",
            "content",
            "page_number",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "modified_at",
        ]


class BookSerializer(serializers.ModelSerializer):
    """serializer for creating book"""

    class Meta:
        model = doccoon
        fields = [
            "id",
            "title",
            "description",
            "year",
            "status",
        ]
        read_only_fields = [
            "id",
            "author",
            "created_at",
            "modified_at",
            "status",
        ]

    def validate_year(self, value):
        current_year = datetime.now().year

        if len(str(value)) != 4 or not str(value).isdigit():
            raise serializers.ValidationError("Year must be 4 digits")

        if value < 1900 or value > current_year:
            raise serializers.ValidationError(
                f"Year must be between 1900 and {current_year}"
            )

        return value

    def validate_title(self, value: str) -> str:
        """Sanitize title to prevent XSS attacks."""
        return sanitize_plain_text(value)

    def validate_description(self, value: str) -> str:
        """Sanitize description to prevent XSS attacks."""
        if value:
            return sanitize_plain_text(value)
        return value


class BookListSerializer(BookSerializer):
    """Serializer for listing books with computed stats.

    IMPORTANT: The queryset must use prefetch_related('doccoonpage_set') for optimal performance.
    This serializer uses the prefetched pages to compute stats without additional queries.
    """

    page_count = serializers.SerializerMethodField()
    image_count = serializers.SerializerMethodField()
    book_size = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = doccoon
        fields = BookSerializer.Meta.fields + [
            "page_count",
            "image_count",
            "book_size",
            "created_at",
            "modified_at",
        ]
        read_only_fields = BookSerializer.Meta.read_only_fields + [
            "page_count",
            "image_count",
            "book_size",
            "created_at",
            "modified_at",
        ]

    def _get_active_pages(self, obj) -> list:
        """Get active pages from prefetched data to avoid N+1 queries."""
        # Use prefetched data if available (from prefetch_related)
        if (
            hasattr(obj, "_prefetched_objects_cache")
            and "doccoonpage_set" in obj._prefetched_objects_cache
        ):
            return [p for p in obj.doccoonpage_set.all() if not p.is_deleted]
        # Fallback: filter in DB (slower, but works without prefetch)
        return list(obj.doccoonpage_set.filter(is_deleted=False))

    def get_page_count(self, obj) -> int:
        if hasattr(obj, "_page_count"):
            return obj._page_count
        return len(self._get_active_pages(obj))

    def get_image_count(self, obj) -> int:
        pages = self._get_active_pages(obj)
        return sum(len(IMAGE_PATTERN.findall(page.content or "")) for page in pages)

    def get_book_size(self, obj) -> int:
        pages = self._get_active_pages(obj)
        return sum(len((page.content or "").encode("utf-8")) for page in pages)


class GetBookWithPagesSerializer(BookSerializer):
    """Serializer for book detail with pages.

    IMPORTANT: The queryset should use prefetch_related('doccoonpage_set') for optimal performance.
    """

    pages = serializers.SerializerMethodField()

    class Meta:
        model = doccoon
        fields = BookSerializer.Meta.fields + ["pages"]
        read_only_fields = BookSerializer.Meta.read_only_fields + ["pages"]

    def get_pages(self, obj):
        # Use prefetched data if available
        if (
            hasattr(obj, "_prefetched_objects_cache")
            and "doccoonpage_set" in obj._prefetched_objects_cache
        ):
            pages = [p for p in obj.doccoonpage_set.all() if not p.is_deleted]
            pages.sort(key=lambda p: p.page_number)
            return PageSerializer(pages, many=True).data
        # Fallback to service function
        return PageSerializer(get_book_pages(obj.id), many=True).data
