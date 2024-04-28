from django.conf import settings
from django.db.models import CASCADE, CharField, ForeignKey, TextChoices, URLField
from django.utils.translation import gettext_lazy as _

from base.models import TimeStampedModel, UUIDModel


class Ride(TimeStampedModel, UUIDModel):
    """
    Model for representing rides.

    Attributes:
    rider (ForeignKey): The user who requested the ride.
    driver (ForeignKey): The user who is assigned as the driver for the ride.
    pickup_location (URLField): The URL for the pickup location.
    dropoff_location (URLField): The URL for the dropoff location.
    status (CharField): The status of the ride, chosen from predefined choices.
    """

    class RideStatus(TextChoices):
        """
        Choices for the status of a ride.
        """

        NOT_STARTED = "not_started", _("Not Started")
        STARTED = "started", _("Started")
        REQUESTED = "requested", _("Requested")
        ACCEPTED = "accepted", _("Accepted")
        COMPLETED = "completed", _("Completed")
        CANCELLED = "cancelled ", _("Cancelled")

    rider = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="rides_as_rider",
        limit_choices_to={"is_superuser": False, "is_driver": False},
    )
    driver = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="rides_as_driver",
        limit_choices_to={"is_superuser": False, "is_driver": True},
    )
    pickup_location = URLField(_("Pickup location"))
    dropoff_location = URLField(_("Dropoff location"))
    status = CharField(
        _("Ride status"),
        max_length=20,
        choices=RideStatus.choices,
        default=RideStatus.NOT_STARTED,
    )

    def __str__(self):
        return f"Ride of {self.rider} - {self.status}"
