import logging
import time
from typing import Callable

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger("doccoon.requests")


class RequestLoggingMiddleware:
    """
    Middleware to log HTTP requests and responses for debugging and monitoring.

    Logs:
    - Request method, path, and user
    - Response status code
    - Request duration in milliseconds
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Skip logging for static files and health checks
        if self._should_skip(request.path):
            return self.get_response(request)

        start_time = time.time()

        # Get user identifier
        user_id = self._get_user_id(request)

        response = self.get_response(request)

        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000

        # Log the request
        self._log_request(request, response, user_id, duration_ms)

        return response

    def _should_skip(self, path: str) -> bool:
        """Skip logging for certain paths."""
        skip_paths = [
            "/health/",
            "/static/",
            "/media/",
            "/__debug__/",
            "/favicon.ico",
        ]
        return any(path.startswith(p) for p in skip_paths)

    def _get_user_id(self, request: HttpRequest) -> str:
        """Get a user identifier for logging."""
        if hasattr(request, "user") and request.user.is_authenticated:
            return f"user:{request.user.id}"
        return "anonymous"

    def _log_request(
        self,
        request: HttpRequest,
        response: HttpResponse,
        user_id: str,
        duration_ms: float,
    ) -> None:
        """Log the request details."""
        log_data = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_ms": round(duration_ms, 2),
            "user": user_id,
        }

        # Add query params if present (but not sensitive data)
        if request.GET and not self._has_sensitive_params(request.GET):
            log_data["query"] = dict(request.GET)

        # Determine log level based on status code
        if response.status_code >= 500:
            logger.error(
                "Request failed: %(method)s %(path)s", log_data, extra=log_data
            )
        elif response.status_code >= 400:
            logger.warning(
                "Request error: %(method)s %(path)s", log_data, extra=log_data
            )
        else:
            logger.info(
                "%(method)s %(path)s %(status)s %(duration_ms).2fms",
                log_data,
                extra=log_data,
            )

    def _has_sensitive_params(self, params: dict) -> bool:
        """Check if query params contain sensitive data."""
        sensitive_keys = {"password", "token", "key", "secret", "api_key"}
        return bool(sensitive_keys & set(k.lower() for k in params.keys()))
