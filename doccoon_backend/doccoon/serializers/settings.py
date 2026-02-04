from rest_framework import serializers

from doccoon.models.settings import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = [
            "id",
            "auto_save_enabled",
            "auto_save_interval",
            "notification_enabled",
            "theme",
            "profile_visible",
            "view_mode",
            "layout_mode",
            "live_preview",
        ]
        read_only_fields = ["id"]
