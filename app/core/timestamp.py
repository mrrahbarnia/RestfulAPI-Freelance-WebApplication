from django.db import models


class TimeStamp(models.Model):
    """Base model for inheriting in other models."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True