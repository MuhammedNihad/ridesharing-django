import uuid

from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CharField,
    EmailField,
    UUIDField,
)
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Default custom user model.
    """

    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None
    last_name = None
    username = None
    email = EmailField(_("Email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """
        Return the string representation of the object.
        """
        return self.email
