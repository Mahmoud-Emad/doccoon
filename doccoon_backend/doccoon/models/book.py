from django.db import models

from doccoon.models.abstracts import DoccoonBaseModel
from doccoon.models.user import User


class BOOK_STATUS(models.TextChoices):
    """enum class for team options"""

    Draft = "Draft"
    Published = "Published"
    Deleted = "Deleted"


class doccoon(DoccoonBaseModel):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    description = models.TextField(blank=True, default="")
    year = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=BOOK_STATUS.choices,
        default=BOOK_STATUS.Draft,
        db_index=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["author", "status", "is_deleted"]),
            models.Index(fields=["author", "is_deleted", "-created_at"]),
        ]

    def __str__(self):
        return self.title


class DoccoonPage(DoccoonBaseModel):
    book = models.ForeignKey(doccoon, on_delete=models.CASCADE, db_index=True)
    content = models.TextField(blank=True, default="")
    page_number = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=["book", "is_deleted", "page_number"]),
        ]
        ordering = ["page_number"]

    def __str__(self):
        return f"Page {self.page_number} of {self.book.title}"
