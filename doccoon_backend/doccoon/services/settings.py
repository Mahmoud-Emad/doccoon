from doccoon.models.settings import UserSettings
from doccoon.models.user import User


def get_or_create_settings(user: User) -> UserSettings:
    settings, _ = UserSettings.objects.get_or_create(user=user)
    return settings
