import logging
import time
from typing import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger("doccoon.requests")

# Pre-compile skip paths as a tuple for faster checking
SKIP_PATH_PREFIXES = (
    "/health/",
    "/static/",
    "/media/",
    "/__debug__/",
    "/favicon.ico",
)

# Pre-compile sensitive keys as a frozenset
SENSITIVE_KEYS = frozenset({"password", "token", "key", "secret", "api_key"})


class RequestLoggingMiddleware:
    """
    Middleware to log HTTP requests and responses for debugging and monitoring.

    Logs:
    - Request method, path, and user
    - Response status code
    - Request duration in milliseconds

    Optimized for minimal overhead in production.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response
        # Cache whether we're in debug mode
        self._debug = settings.DEBUG

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Fast path: skip logging for static files and health checks
        path = request.path
        if path.startswith(SKIP_PATH_PREFIXES):
            return self.get_response(request)

        start_time = time.perf_counter()  # More precise than time.time()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Only log if response warrants it (errors or debug mode or slow requests)
        status = response.status_code
        if status >= 400 or self._debug or duration_ms > 1000:
            self._log_request(request, response, duration_ms)

        return response

    def _log_request(
        self,
        request: HttpRequest,
        response: HttpResponse,
        duration_ms: float,
    ) -> None:
        """Log the request details."""
        # Get user ID lazily and efficiently
        user_id = "anonymous"
        if hasattr(request, "user"):
            user = request.user
            if hasattr(user, "is_authenticated") and user.is_authenticated:
                user_id = f"user:{user.id}"

        method = request.method
        path = request.path
        status = response.status_code

        # Determine log level based on status code
        if status >= 500:
            logger.error(f"Request failed: {method} {path}")
        elif status >= 400:
            logger.warning(f"Request error: {method} {path}")
        else:
            logger.info(f"{method} {path} {status} {duration_ms:.2f}ms")
