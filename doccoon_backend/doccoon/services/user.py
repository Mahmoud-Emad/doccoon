from typing import Optional

from doccoon.models.user import User


def get_user_by_id(id: int) -> Optional[User]:
    """Return active, non-deleted user if exists, else None."""
    try:
        return User.objects.get(id=int(id), is_deleted=False, is_active=True)
    except User.DoesNotExist:
        return None


def get_user_by_email(email: str) -> Optional[User]:
    """Return non-deleted user by email if exists, else None."""
    try:
        return User.objects.get(email=email, is_deleted=False)
    except User.DoesNotExist:
        return None
