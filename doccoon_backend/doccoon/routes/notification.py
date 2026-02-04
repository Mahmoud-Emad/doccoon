from django.urls import path

from doccoon.views.notification import (
    NotificationDetailApiView,
    NotificationListApiView,
    NotificationReadAllApiView,
)

urlpatterns = [
    path("", NotificationListApiView.as_view()),
    path("read-all/", NotificationReadAllApiView.as_view()),
    path("<int:notification_id>/read/", NotificationDetailApiView.as_view()),
    path("<int:notification_id>/", NotificationDetailApiView.as_view()),
]
