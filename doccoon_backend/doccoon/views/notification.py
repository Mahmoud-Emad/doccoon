from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request

from doccoon.api.permissions import UserIsAuthenticated
from doccoon.api.response import CustomResponse
from doccoon.serializers.notification import NotificationSerializer
from doccoon.services.notification import (
    get_notification_by_id,
    get_user_notifications,
)

# ======================================================
# Notifications: List
# ======================================================


@swagger_auto_schema(tags=["Notifications"])
class NotificationListApiView(ListAPIView):
    """List all notifications for the authenticated user."""

    serializer_class = NotificationSerializer
    permission_classes = [UserIsAuthenticated]

    def get_queryset(self):
        return get_user_notifications(self.request.user)


# ======================================================
# Notifications: Mark Read / Delete
# ======================================================


@swagger_auto_schema(tags=["Notifications"])
class NotificationDetailApiView(GenericAPIView):
    """Mark a notification as read or delete it."""

    permission_classes = [UserIsAuthenticated]

    def put(self, request: Request, notification_id: int) -> CustomResponse:
        notification = get_notification_by_id(notification_id)
        if not notification or notification.user_id != request.user.id:
            return CustomResponse.not_found(message="Notification not found")

        notification.is_read = True
        notification.save()
        return CustomResponse.success(
            data=NotificationSerializer(notification).data,
            message="Notification marked as read.",
        )

    def delete(self, request: Request, notification_id: int) -> CustomResponse:
        notification = get_notification_by_id(notification_id)
        if not notification or notification.user_id != request.user.id:
            return CustomResponse.not_found(message="Notification not found")

        notification.is_deleted = True
        notification.deleted_at = datetime.now()
        notification.save()
        return CustomResponse.success(
            message="Notification deleted successfully.",
            status_code=204,
        )


# ======================================================
# Notifications: Mark All Read
# ======================================================


@swagger_auto_schema(tags=["Notifications"])
class NotificationReadAllApiView(GenericAPIView):
    """Mark all notifications as read."""

    permission_classes = [UserIsAuthenticated]

    def put(self, request: Request) -> CustomResponse:
        get_user_notifications(request.user).filter(is_read=False).update(is_read=True)
        return CustomResponse.success(
            message="All notifications marked as read.",
        )
