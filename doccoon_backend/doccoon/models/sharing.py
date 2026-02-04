import uuid

from django.db import models

from doccoon.models.abstracts import DoccoonBaseModel
from doccoon.models.book import DoccoonPage, doccoon
from doccoon.models.user import User


class SharedBook(DoccoonBaseModel):
    book = models.ForeignKey(doccoon, on_delete=models.CASCADE, related_name="shares")
    shared_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shared_books"
    )
    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    pages_snapshot = models.JSONField(default=list, blank=True)

    class Meta:
        unique_together = ["book", "shared_by"]

    def __str__(self):
        return f"Shared book: {self.book.title} by {self.shared_by.email}"


class SharedPage(DoccoonBaseModel):
    page = models.ForeignKey(
        DoccoonPage, on_delete=models.CASCADE, related_name="shares"
    )
    book = models.ForeignKey(
        doccoon, on_delete=models.CASCADE, related_name="page_shares"
    )
    shared_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shared_pages"
    )
    share_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    content_snapshot = models.TextField(blank=True, default="")

    class Meta:
        unique_together = ["page", "shared_by"]

    def __str__(self):
        return f"Shared page: {self.page} by {self.shared_by.email}"
