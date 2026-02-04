from typing import Optional

from django.db.models import QuerySet

from doccoon.models.book import DoccoonPage, doccoon
from doccoon.models.notification import NOTIFICATION_TYPE, Notification
from doccoon.models.user import User


def create_notification(
    user: User,
    notification_type: str,
    title: str,
    message: str,
    related_book: Optional[doccoon] = None,
    related_page: Optional[DoccoonPage] = None,
) -> Notification:
    return Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        message=message,
        related_book=related_book,
        related_page=related_page,
    )


def get_user_notifications(user: User) -> QuerySet:
    return Notification.objects.filter(user=user, is_deleted=False).order_by(
        "-created_at"
    )


def get_notification_by_id(notification_id: int) -> Optional[Notification]:
    try:
        return Notification.objects.get(id=notification_id, is_deleted=False)
    except Notification.DoesNotExist:
        return None
