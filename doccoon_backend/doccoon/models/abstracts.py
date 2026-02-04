"""abstract model for created, updated timestamps"""

from django.db import models


class DoccoonBaseModel(models.Model):
    """Database model for created and updated timestamps"""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"""created at : {self.created_at} ,
            modified at : {self.modified_at}"""