from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Ride

User = get_user_model()


class RideModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )

    def test_ride_creation(self):
        ride = Ride.objects.create(
            rider=self.user,
            pickup_location="https://maps.app.goo.gl/6HLE7nEFM5zADR377",
            dropoff_location="https://maps.app.goo.gl/VCnHJfMwSV7K17wK6",
            status=Ride.RideStatus.REQUESTED,
        )
        self.assertEqual(ride.status, Ride.RideStatus.REQUESTED)
        self.assertEqual(ride.rider, self.user)

    def test_default_status(self):
        ride = Ride.objects.create(
            rider=self.user,
            pickup_location="https://maps.app.goo.gl/6HLE7nEFM5zADR377",
            dropoff_location="https://maps.app.goo.gl/VCnHJfMwSV7K17wK6",
        )
        self.assertEqual(ride.status, Ride.RideStatus.NOT_STARTED)

    def test_str_method(self):
        ride = Ride.objects.create(
            rider=self.user,
            pickup_location="https://maps.app.goo.gl/6HLE7nEFM5zADR377",
            dropoff_location="https://maps.app.goo.gl/VCnHJfMwSV7K17wK6",
        )
        self.assertEqual(
            str(ride), f"Ride of {self.user} - {Ride.RideStatus.NOT_STARTED}"
        )
