"""Test settings - inherits from main settings with test-specific overrides."""

from config.settings import *  # noqa: F401, F403

# Completely replace REST_FRAMEWORK to disable throttling
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    # No throttle classes
}

# Use in-memory SQLite for faster tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable debug mode to skip debug_toolbar URL imports
DEBUG = False
