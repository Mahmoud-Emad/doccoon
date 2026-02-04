from django.db import models

from doccoon.models.abstracts import DoccoonBaseModel
from doccoon.models.book import DoccoonPage, doccoon
from doccoon.models.user import User


class NOTIFICATION_TYPE(models.TextChoices):
    BookShared = "BookShared"
    PageShared = "PageShared"
    BookPublished = "BookPublished"
    AIRefineComplete = "AIRefineComplete"
    General = "General"


class Notification(DoccoonBaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications", db_index=True
    )
    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPE.choices,
        default=NOTIFICATION_TYPE.General,
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    related_book = models.ForeignKey(
        doccoon, on_delete=models.SET_NULL, null=True, blank=True
    )
    related_page = models.ForeignKey(
        DoccoonPage, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["user", "is_deleted", "-created_at"]),
            models.Index(fields=["user", "is_read", "is_deleted"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification: {self.title} for {self.user.email}"
