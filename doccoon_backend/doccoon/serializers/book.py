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
    """Serializer for listing books with computed stats."""

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

    def get_page_count(self, obj) -> int:
        if hasattr(obj, "_page_count"):
            return obj._page_count
        return obj.doccoonpage_set.filter(is_deleted=False).count()

    def get_image_count(self, obj) -> int:
        total = 0
        pages = obj.doccoonpage_set.filter(is_deleted=False)
        for page in pages:
            total += len(IMAGE_PATTERN.findall(page.content or ""))
        return total

    def get_book_size(self, obj) -> int:
        total = 0
        pages = obj.doccoonpage_set.filter(is_deleted=False)
        for page in pages:
            total += len((page.content or "").encode("utf-8"))
        return total


class GetBookWithPagesSerializer(BookSerializer):
    pages = serializers.SerializerMethodField()

    class Meta:
        model = doccoon
        fields = BookSerializer.Meta.fields + ["pages"]
        read_only_fields = BookSerializer.Meta.read_only_fields + ["pages"]

    def get_pages(self, obj):
        return PageSerializer(get_book_pages(obj.id), many=True).data
