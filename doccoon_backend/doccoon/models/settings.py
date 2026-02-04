from django.db import models

from doccoon.models.abstracts import DoccoonBaseModel
from doccoon.models.user import User


class UserSettings(DoccoonBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    auto_save_enabled = models.BooleanField(default=True)
    auto_save_interval = models.IntegerField(default=2)  # seconds
    notification_enabled = models.BooleanField(default=True)
    theme = models.CharField(
        max_length=10,
        default="light",
        choices=[("light", "Light"), ("dark", "Dark")],
    )
    profile_visible = models.BooleanField(default=True)
    view_mode = models.BooleanField(default=False)  # False = edit, True = view
    layout_mode = models.CharField(
        max_length=10,
        default="book",
        choices=[("book", "Book"), ("page", "Page")],
    )
    live_preview = models.BooleanField(default=False)

    def __str__(self):
        return f"Settings for {self.user.email}"
