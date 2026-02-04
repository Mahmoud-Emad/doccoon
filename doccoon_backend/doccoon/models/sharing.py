import uuid

from django.db import models

from doccoon.models.abstracts import DoccoonBaseModel
from doccoon.models.book import DoccoonPage, doccoon
from doccoon.models.user import User


class SharedBook(DoccoonBaseModel):
    book = models.ForeignKey(
        doccoon, on_delete=models.CASCADE, related_name="shares", db_index=True
    )
    shared_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shared_books", db_index=True
    )
    share_token = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, db_index=True
    )
    is_active = models.BooleanField(default=True, db_index=True)
    pages_snapshot = models.JSONField(default=list, blank=True)

    class Meta:
        unique_together = ["book", "shared_by"]
        indexes = [
            models.Index(fields=["share_token", "is_active"]),
        ]

    def __str__(self):
        return f"Shared book: {self.book.title} by {self.shared_by.email}"


class SharedPage(DoccoonBaseModel):
    page = models.ForeignKey(
        DoccoonPage, on_delete=models.CASCADE, related_name="shares", db_index=True
    )
    book = models.ForeignKey(
        doccoon, on_delete=models.CASCADE, related_name="page_shares", db_index=True
    )
    shared_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shared_pages", db_index=True
    )
    share_token = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, db_index=True
    )
    is_active = models.BooleanField(default=True, db_index=True)
    content_snapshot = models.TextField(blank=True, default="")

    class Meta:
        unique_together = ["page", "shared_by"]
        indexes = [
            models.Index(fields=["share_token", "is_active"]),
        ]

    def __str__(self):
        return f"Shared page: {self.page} by {self.shared_by.email}"
