from rest_framework import serializers

from doccoon.models.user import User
from doccoon.utils.sanitize import sanitize_plain_text


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    has_password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "full_name", "has_password"]
        read_only_fields = ["id", "email", "full_name", "has_password"]

    def get_has_password(self, obj) -> bool:
        return obj.has_usable_password()


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]

    def validate_first_name(self, value: str) -> str:
        """Sanitize first name to prevent XSS attacks."""
        if value:
            return sanitize_plain_text(value)
        return value

    def validate_last_name(self, value: str) -> str:
        """Sanitize last name to prevent XSS attacks."""
        if value:
            return sanitize_plain_text(value)
        return value
