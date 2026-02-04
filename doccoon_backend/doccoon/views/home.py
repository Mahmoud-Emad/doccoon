from django.conf import settings
from django.db import connections
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from components import config
from doccoon.api.response import CustomResponse


class HomeApiView(APIView):
    @swagger_auto_schema(tags=["Home"])
    def get(self, request):
        return CustomResponse.success(
            message="Server is up and running",
            status_code=200,
            data={
                "routes": {
                    "health": "/health",
                    "health_live": "/health/live",
                    "health_ready": "/health/ready",
                    "admin": "/admin",
                    "swagger": "/swagger",
                    "redoc": "/redoc",
                    "api": {
                        "auth": "/api/auth",
                        "books": "/api/books",
                        "users": "/api/users",
                    },
                }
            },
        )


class HealthLiveApiView(APIView):
    """
    Kubernetes liveness probe endpoint.
    Returns 200 if the application is running.
    Used by load balancers and orchestrators to check if the container is alive.
    """

    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(tags=["Health"])
    def get(self, request):
        return JsonResponse({"status": "ok"}, status=200)


class HealthReadyApiView(APIView):
    """
    Kubernetes readiness probe endpoint.
    Returns 200 if the application is ready to serve traffic.
    Checks database connectivity.
    """

    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(tags=["Health"])
    def get(self, request):
        try:
            # Check database connection
            connections["default"].ensure_connection()
            return JsonResponse({"status": "ok", "database": "connected"}, status=200)
        except Exception as e:
            return JsonResponse(
                {"status": "error", "database": "disconnected", "error": str(e)},
                status=503,
            )


class HealthApiView(APIView):
    """
    Detailed health check endpoint.
    Returns comprehensive health information about all services.
    """

    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(tags=["Health"])
    def get(self, request):
        # Check all services
        services_status = {
            "database": self._check_database(),
            "email": self._check_email(),
        }

        # Overall health status
        overall_health = all(service["status"] for service in services_status.values())

        status_code = 200 if overall_health else 503

        return JsonResponse(
            {
                "healthy": overall_health,
                "environment": config("ENV", default="development"),
                "services": services_status,
            },
            status=status_code,
        )

    def _check_database(self):
        """Check if the database is accessible"""
        try:
            # Try to connect to the database
            connections["default"].ensure_connection()
            # Get database info (only non-sensitive information)
            db_info = {
                "engine": settings.DATABASES["default"]["ENGINE"].split(".")[-1],
            }

            # For security, we don't expose the full database path or connection details
            if "sqlite3" in settings.DATABASES["default"]["ENGINE"]:
                db_info["type"] = "SQLite"
            elif "postgresql" in settings.DATABASES["default"]["ENGINE"]:
                db_info["type"] = "PostgreSQL"

            return {
                "status": True,
                "message": "Database connection successful",
                "info": db_info,
            }
        except Exception as e:
            return {
                "status": False,
                "message": f"Database connection failed: {str(e)}",
                "info": {
                    "engine": settings.DATABASES["default"]["ENGINE"].split(".")[-1]
                },
            }

    def _check_email(self):
        """Check if email service is configured correctly"""
        try:
            # Check if email settings are configured
            if not all(
                [
                    settings.EMAIL_HOST,
                    settings.EMAIL_PORT,
                    settings.EMAIL_HOST_USER,
                    settings.EMAIL_HOST_PASSWORD,
                ]
            ):
                return {
                    "status": False,
                    "message": "Email service is not fully configured",
                    "info": {"service": "Email", "configured": False},
                }

            # We don't actually connect to the SMTP server to avoid potential issues
            # Just check if the configuration exists
            # For security, we don't expose the actual email credentials
            return {
                "status": True,
                "message": "Email service is configured",
                "info": {
                    "service": "Email",
                    "configured": True,
                    "provider": (
                        settings.EMAIL_HOST.split(".")[0]
                        if "." in settings.EMAIL_HOST
                        else settings.EMAIL_HOST
                    ),
                },
            }
        except Exception as e:
            return {
                "status": False,
                "message": f"Email service check failed: {str(e)}",
                "info": {"service": "Email", "configured": False},
            }
