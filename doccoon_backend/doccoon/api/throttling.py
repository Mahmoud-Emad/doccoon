from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AuthAnonThrottle(AnonRateThrottle):
    """Stricter rate limit for anonymous auth endpoints (login, signup)."""

    rate = "5/minute"


class AuthUserThrottle(UserRateThrottle):
    """Stricter rate limit for authenticated auth endpoints (password change)."""

    rate = "10/minute"


class AIRateThrottle(UserRateThrottle):
    """Rate limit for AI endpoints to control costs."""

    rate = "20/minute"


class AIAnonThrottle(AnonRateThrottle):
    """Rate limit for anonymous AI demo endpoints."""

    rate = "5/minute"


class PageOperationThrottle(UserRateThrottle):
    """Rate limit for page CRUD operations."""

    rate = "60/minute"


class BookOperationThrottle(UserRateThrottle):
    """Rate limit for book CRUD operations."""

    rate = "30/minute"


class SettingsThrottle(UserRateThrottle):
    """Rate limit for settings updates."""

    rate = "20/minute"


class SharingThrottle(UserRateThrottle):
    """Rate limit for sharing operations."""

    rate = "30/minute"


class BurstAnonThrottle(AnonRateThrottle):
    """Burst protection for anonymous users - prevents rapid-fire requests."""

    rate = "10/minute"


class BurstUserThrottle(UserRateThrottle):
    """Burst protection for authenticated users - prevents rapid-fire requests."""

    rate = "60/minute"
