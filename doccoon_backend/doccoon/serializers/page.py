from rest_framework import serializers

from doccoon.models.book import DoccoonPage
from doccoon.utils.sanitize import sanitize_markdown


class CreatePageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False, allow_blank=True, default="")

    class Meta:
        model = DoccoonPage
        fields = ["id", "content", "page_number"]
        read_only_fields = ["id", "page_number"]

    def validate_content(self, value: str) -> str:
        """Sanitize content to prevent XSS attacks."""
        return sanitize_markdown(value)


class UpdatePageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = DoccoonPage
        fields = ["id", "content", "page_number"]
        read_only_fields = ["id"]

    def validate_content(self, value: str) -> str:
        """Sanitize content to prevent XSS attacks."""
        return sanitize_markdown(value)


class PageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoccoonPage
        fields = [
            "id",
            "content",
            "page_number",
            "created_at",
            "modified_at",
        ]
        read_only_fields = fields
