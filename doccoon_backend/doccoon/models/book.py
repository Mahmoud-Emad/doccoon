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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, default="")
    year = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=BOOK_STATUS.choices, default=BOOK_STATUS.Draft
    )

    def __str__(self):
        return self.title


class DoccoonPage(DoccoonBaseModel):
    book = models.ForeignKey(doccoon, on_delete=models.CASCADE)
    content = models.TextField(blank=True, default="")
    page_number = models.IntegerField()

    def __str__(self):
        return f"Page {self.page_number} of {self.book.title}"
