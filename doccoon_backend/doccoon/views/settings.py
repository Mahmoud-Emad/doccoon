from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from doccoon.api.permissions import UserIsAuthenticated
from doccoon.api.response import CustomResponse
from doccoon.api.throttling import SettingsThrottle
from doccoon.serializers.settings import UserSettingsSerializer
from doccoon.services.settings import get_or_create_settings


@swagger_auto_schema(tags=["Settings"])
class UserSettingsApiView(GenericAPIView):
    """Get or update user settings."""

    permission_classes = [UserIsAuthenticated]
    serializer_class = UserSettingsSerializer
    throttle_classes = [SettingsThrottle]

    def get(self, request: Request) -> CustomResponse:
        settings = get_or_create_settings(request.user)
        serializer = UserSettingsSerializer(settings)
        return CustomResponse.success(
            data=serializer.data,
            message="Settings retrieved successfully.",
        )

    def put(self, request: Request) -> CustomResponse:
        settings = get_or_create_settings(request.user)
        serializer = UserSettingsSerializer(settings, data=request.data, partial=True)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Invalid data",
                data=serializer.errors,
            )
        serializer.save()
        return CustomResponse.success(
            data=serializer.data,
            message="Settings updated successfully.",
        )
