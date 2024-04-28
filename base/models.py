import uuid

from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-managed created_at and updated_at timestamp fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """
    An abstract base class model that provides uuid field as primary key.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
