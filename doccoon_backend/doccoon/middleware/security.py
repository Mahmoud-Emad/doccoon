"""
Security middleware for adding CSP and other security headers.
"""

from django.conf import settings


class ContentSecurityPolicyMiddleware:
    """
    Middleware to add Content-Security-Policy headers to responses.

    CSP helps prevent XSS attacks by specifying which sources of content
    are allowed to be loaded by the browser.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Build CSP directives
        # In production, this should be stricter
        self.csp_directives = {
            "default-src": ["'self'"],
            "script-src": [
                "'self'",
                "'unsafe-inline'",
                "'unsafe-eval'",
            ],  # Required for some JS libs
            "style-src": ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
            "font-src": ["'self'", "https://fonts.gstatic.com", "data:"],
            "img-src": ["'self'", "data:", "blob:", "https:"],
            "connect-src": ["'self'", "https:"],
            "frame-ancestors": ["'none'"],
            "form-action": ["'self'"],
            "base-uri": ["'self'"],
            "object-src": ["'none'"],
        }

    def __call__(self, request):
        response = self.get_response(request)

        # Only add CSP in production
        if not settings.DEBUG:
            csp_header = self._build_csp_header()
            response["Content-Security-Policy"] = csp_header

        # Always add Permissions-Policy header
        response["Permissions-Policy"] = (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=()"
        )

        return response

    def _build_csp_header(self) -> str:
        """Build the CSP header string from directives."""
        parts = []
        for directive, sources in self.csp_directives.items():
            parts.append(f"{directive} {' '.join(sources)}")
        return "; ".join(parts)
