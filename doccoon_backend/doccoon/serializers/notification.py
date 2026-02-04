from rest_framework import serializers

from doccoon.models.notification import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "title",
            "message",
            "is_read",
            "related_book",
            "related_page",
            "created_at",
        ]
        read_only_fields = fields
