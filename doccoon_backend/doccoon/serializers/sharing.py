from rest_framework import serializers

from doccoon.models.sharing import SharedBook, SharedPage


class SharedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedBook
        fields = ["id", "share_token", "is_active", "created_at"]
        read_only_fields = fields


class SharedPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedPage
        fields = ["id", "share_token", "is_active", "created_at"]
        read_only_fields = fields


class PublicBookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="book.title", read_only=True)
    description = serializers.CharField(source="book.description", read_only=True)
    year = serializers.IntegerField(source="book.year", read_only=True)
    status = serializers.CharField(source="book.status", read_only=True)
    pages = serializers.JSONField(source="pages_snapshot", read_only=True)

    class Meta:
        model = SharedBook
        fields = ["id", "title", "description", "year", "status", "pages"]
        read_only_fields = fields


class PublicPageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(source="content_snapshot", read_only=True)
    page_number = serializers.IntegerField(source="page.page_number", read_only=True)
    book_title = serializers.CharField(source="page.book.title", read_only=True)
    book_is_public = serializers.SerializerMethodField()

    class Meta:
        model = SharedPage
        fields = [
            "id",
            "content",
            "page_number",
            "book_title",
            "book_is_public",
            "created_at",
            "modified_at",
        ]
        read_only_fields = fields

    def get_book_is_public(self, obj):
        return obj.page.book.status == "Published"
