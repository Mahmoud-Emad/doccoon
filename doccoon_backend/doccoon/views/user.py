from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from doccoon.api.permissions import UserIsAuthenticated
from doccoon.api.response import CustomResponse
from doccoon.serializers.user import UserProfileSerializer, UserProfileUpdateSerializer


@swagger_auto_schema(tags=["User"])
class UserProfileApiView(GenericAPIView):
    """Get or update user profile."""

    permission_classes = [UserIsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request: Request) -> CustomResponse:
        serializer = UserProfileSerializer(request.user)
        return CustomResponse.success(
            data=serializer.data,
            message="Profile retrieved successfully.",
        )

    def put(self, request: Request) -> CustomResponse:
        serializer = UserProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Invalid data",
                data=serializer.errors,
            )
        serializer.save()
        return CustomResponse.success(
            data=UserProfileSerializer(request.user).data,
            message="Profile updated successfully.",
        )
