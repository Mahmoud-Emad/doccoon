import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(
    self,
    subject: str,
    message: str,
    recipient_list: list[str],
    html_message: str | None = None,
):
    """
    Generic task to send an email asynchronously.

    Args:
        subject: Email subject
        message: Plain text email body
        recipient_list: List of recipient email addresses
        html_message: Optional HTML email body
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {recipient_list}")
    except Exception as exc:
        logger.error(f"Failed to send email to {recipient_list}: {exc}")
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email_task(self, email: str, first_name: str, reset_url: str):
    """
    Task to send password reset email asynchronously.

    Args:
        email: Recipient email address
        first_name: User's first name for personalization
        reset_url: Password reset URL
    """
    subject = "Reset your Doccoon password"
    message = f"""Hi {first_name},

You requested to reset your password for your Doccoon account.

Click the link below to reset your password:
{reset_url}

This link will expire in 24 hours.

If you didn't request this, you can safely ignore this email.

Best,
The Doccoon Team
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"Password reset email sent to {email}")
    except Exception as exc:
        logger.error(f"Failed to send password reset email to {email}: {exc}")
        raise self.retry(exc=exc)
