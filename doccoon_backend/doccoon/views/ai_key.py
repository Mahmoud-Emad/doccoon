from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from doccoon.api.permissions import UserIsAuthenticated
from doccoon.api.response import CustomResponse
from doccoon.models.ai_provider_key import AIProviderKey
from doccoon.serializers.ai_provider_key import (
    AIProviderKeyCreateSerializer,
    AIProviderKeySerializer,
)


@swagger_auto_schema(tags=["AI Keys"])
class AIProviderKeyListCreateApiView(GenericAPIView):
    """List and create AI provider keys."""

    permission_classes = [UserIsAuthenticated]
    serializer_class = AIProviderKeySerializer

    def get(self, request: Request) -> CustomResponse:
        keys = AIProviderKey.objects.filter(user=request.user, is_deleted=False)
        serializer = AIProviderKeySerializer(keys, many=True)
        return CustomResponse.success(
            data=serializer.data,
            message="AI keys retrieved successfully.",
        )

    def post(self, request: Request) -> CustomResponse:
        serializer = AIProviderKeyCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Invalid data",
                data=serializer.errors,
            )
        key = serializer.save(user=request.user)
        return CustomResponse.success(
            data=AIProviderKeySerializer(key).data,
            message="AI key created successfully.",
            status_code=201,
        )


@swagger_auto_schema(tags=["AI Keys"])
class AIProviderKeyDetailApiView(GenericAPIView):
    """Update or delete an AI provider key."""

    permission_classes = [UserIsAuthenticated]
    serializer_class = AIProviderKeySerializer

    def _get_key(self, request: Request, key_id: int):
        try:
            return AIProviderKey.objects.get(
                id=key_id, user=request.user, is_deleted=False
            )
        except AIProviderKey.DoesNotExist:
            return None

    def put(self, request: Request, key_id: int) -> CustomResponse:
        key = self._get_key(request, key_id)
        if not key:
            return CustomResponse.not_found(message="AI key not found.")
        serializer = AIProviderKeyCreateSerializer(key, data=request.data, partial=True)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                message="Invalid data",
                data=serializer.errors,
            )
        serializer.save()
        return CustomResponse.success(
            data=AIProviderKeySerializer(key).data,
            message="AI key updated successfully.",
        )

    def delete(self, request: Request, key_id: int) -> CustomResponse:
        key = self._get_key(request, key_id)
        if not key:
            return CustomResponse.not_found(message="AI key not found.")
        from django.utils import timezone

        key.is_deleted = True
        key.deleted_at = timezone.now()
        key.save()
        return CustomResponse.success(message="AI key deleted successfully.")
