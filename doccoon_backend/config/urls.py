from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config import *
from doccoon.views.home import (
    HealthApiView,
    HealthLiveApiView,
    HealthReadyApiView,
    HomeApiView,
)

urlpatterns = [
    path("", HomeApiView.as_view()),
    path("health/", HealthApiView.as_view()),
    path("health/live/", HealthLiveApiView.as_view()),
    path("health/ready/", HealthReadyApiView.as_view()),
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("auth/", include("doccoon.routes.auth")),
                path("books/", include("doccoon.routes.book")),
                path("settings/", include("doccoon.routes.settings")),
                path("notifications/", include("doccoon.routes.notification")),
                path("shared/", include("doccoon.routes.sharing")),
                path("ai/", include("doccoon.routes.ai")),
                path("auth/social/", include("doccoon.routes.social_auth")),
            ]
        ),
    ),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)


if settings.DEBUG:
    import debug_toolbar
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view

    schema_view = get_schema_view(
        openapi.Info(
            title="Api Documentation",
            default_version="v1",
        ),
        public=False,
    )

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path("__debug__/", include(debug_toolbar.urls)),
        # Swagger
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ] + urlpatterns
