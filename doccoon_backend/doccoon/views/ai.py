import logging

from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.throttling import AnonRateThrottle

from doccoon.api.permissions import UserIsAuthenticated
from doccoon.api.response import CustomResponse
from doccoon.api.throttling import AIRateThrottle
from doccoon.models.notification import NOTIFICATION_TYPE
from doccoon.serializers.ai import AIRefineRequestSerializer
from doccoon.services.ai import refine_content
from doccoon.services.notification import create_notification

logger = logging.getLogger(__name__)


class AIDemoThrottle(AnonRateThrottle):
    """Strict throttle for AI demo endpoint."""

    rate = "10/hour"


def _friendly_ai_error(exc: Exception) -> str:
    """Return a short, user-friendly error message from an AI provider exception."""
    logger.error("AI service error: %s", exc)
    raw = str(exc).lower()

    if isinstance(exc, ValueError):
        return str(exc)

    if "401" in raw or "invalid_api_key" in raw or "incorrect api key" in raw:
        return "Invalid API key. Please check your key in Settings > AI Configuration."
    if (
        "429" in raw
        or "rate_limit" in raw
        or "resource_exhausted" in raw
        or "quota" in raw
    ):
        return "AI rate limit or quota exceeded. Please try again later, or login and add your own API key."
    if "403" in raw or "permission" in raw:
        return "Your API key does not have permission for this model. Check your provider plan."
    if "404" in raw or "model_not_found" in raw or "not found" in raw:
        return "The selected AI model was not found. Please choose a different model in settings."
    if "500" in raw or "internal" in raw or "server_error" in raw:
        return "The AI provider is experiencing issues. Please try again later."
    if "timeout" in raw:
        return "The AI request timed out. Please try again."

    return "Something went wrong with the AI service. Please try again."


@swagger_auto_schema(tags=["AI"])
class AIRefineApiView(GenericAPIView):
    """Refine or rewrite content using AI."""

    permission_classes = [UserIsAuthenticated]
    throttle_classes = [AIRateThrottle]
    serializer_class = AIRefineRequestSerializer

    def post(self, request: Request) -> CustomResponse:
        serializer = AIRefineRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Invalid data",
                data=serializer.errors,
            )

        content = serializer.validated_data["content"]
        mode = serializer.validated_data["mode"]
        context = serializer.validated_data.get("context", "")

        try:
            refined = refine_content(content, mode, context, user=request.user)
        except Exception as e:
            return CustomResponse.bad_request(message=_friendly_ai_error(e))

        create_notification(
            user=request.user,
            notification_type=NOTIFICATION_TYPE.AIRefineComplete,
            title="AI refinement complete",
            message=f"Your content has been {mode}d successfully.",
        )

        return CustomResponse.success(
            data={
                "original": content,
                "refined": refined,
                "mode": mode,
            },
            message="Content refined successfully.",
        )


def _get_client_ip(request: Request) -> str:
    """Extract client IP from request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


DEMO_CACHE_TIMEOUT = 60 * 5  # 5 minutes


@swagger_auto_schema(tags=["AI"])
class AIDemoApiView(GenericAPIView):
    """
    Demo AI endpoint for anonymous users.
    Each IP can use refine once and rewrite once, resetting every 5 minutes.
    """

    throttle_classes = [AIDemoThrottle]
    serializer_class = AIRefineRequestSerializer

    def get(self, request: Request) -> CustomResponse:
        """Get current credit status for the client IP."""
        client_ip = _get_client_ip(request)
        refine_key = f"ai_demo_{client_ip}_refine"
        rewrite_key = f"ai_demo_{client_ip}_rewrite"

        refine_used = cache.get(refine_key) is not None
        rewrite_used = cache.get(rewrite_key) is not None

        return CustomResponse.success(
            data={
                "refine_used": refine_used,
                "rewrite_used": rewrite_used,
                "reset_minutes": DEMO_CACHE_TIMEOUT // 60,
            },
            message="Credit status retrieved.",
        )

    def post(self, request: Request) -> CustomResponse:
        serializer = AIRefineRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Invalid data",
                data=serializer.errors,
            )

        content = serializer.validated_data["content"]
        mode = serializer.validated_data["mode"]
        context = serializer.validated_data.get("context", "")

        # Check if this IP has already used this mode
        client_ip = _get_client_ip(request)
        cache_key = f"ai_demo_{client_ip}_{mode}"

        if cache.get(cache_key):
            return CustomResponse.bad_request(
                message=f"You have already used your free {mode} credit. Credits reset every {DEMO_CACHE_TIMEOUT // 60} minutes.",
                data={
                    "exceeded": True,
                    "mode": mode,
                    "reset_minutes": DEMO_CACHE_TIMEOUT // 60,
                },
            )

        try:
            # Use server's Gemini key (no user passed)
            refined = refine_content(content, mode, context, user=None)
        except Exception as e:
            return CustomResponse.bad_request(message=_friendly_ai_error(e))

        # Mark this mode as used for this IP (expires in 5 minutes)
        cache.set(cache_key, True, timeout=DEMO_CACHE_TIMEOUT)

        return CustomResponse.success(
            data={
                "original": content,
                "refined": refined,
                "mode": mode,
                "reset_minutes": DEMO_CACHE_TIMEOUT // 60,
            },
            message=f"Content {mode}d successfully. Sign up to get unlimited access!",
        )
