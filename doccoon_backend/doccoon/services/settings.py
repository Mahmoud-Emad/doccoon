from django.core.cache import cache

from doccoon.models.settings import UserSettings
from doccoon.models.user import User

SETTINGS_CACHE_TIMEOUT = 300  # 5 minutes


def _settings_cache_key(user_id: int) -> str:
    return f"user_settings:{user_id}"


def get_or_create_settings(user: User) -> UserSettings:
    """Get or create user settings with caching."""
    cache_key = _settings_cache_key(user.id)

    # Try cache first
    settings = cache.get(cache_key)
    if settings is not None:
        return settings

    # Cache miss - get from DB
    settings, _ = UserSettings.objects.get_or_create(user=user)
    cache.set(cache_key, settings, SETTINGS_CACHE_TIMEOUT)
    return settings


def invalidate_settings_cache(user_id: int) -> None:
    """Invalidate settings cache when settings are updated."""
    cache.delete(_settings_cache_key(user_id))
