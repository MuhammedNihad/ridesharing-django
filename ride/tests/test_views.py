from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from ..models import Ride
from ..views import RideModelViewSet

User = get_user_model()


class RideModelViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.driver = User.objects.create_user(
            email="testdriver@example.com", password="testpassword", is_driver=True
        )
        self.ride = Ride.objects.create(
            rider=self.user,
            pickup_location="https://maps.app.goo.gl/6HLE7nEFM5zADR377",
            dropoff_location="https://maps.app.goo.gl/VCnHJfMwSV7K17wK6",
            status=Ride.RideStatus.REQUESTED,
        )

    def test_create_ride(self):
        request = self.factory.post(
            "/ride/",
            {
                "pickup_location": "https://maps.app.goo.gl/6HLE7nEFM5zADR377",
                "dropoff_location": "https://maps.app.goo.gl/VCnHJfMwSV7K17wK6",
                "status": Ride.RideStatus.REQUESTED,
            },
            format="json",
        )
        request.user = self.user
        view = RideModelViewSet.as_view({"post": "create"})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Ride.objects.count(), 2
        )  # Assuming there's already one ride in the database

    def test_accept_ride(self):
        request = self.factory.post(
            f"/ride/{self.ride.id}/accept_ride/",
            {"status": Ride.RideStatus.ACCEPTED},
            format="json",
        )
        request.user = self.driver
        view = RideModelViewSet.as_view({"post": "accept_ride"})
        response = view(request, pk=self.ride.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Ride.objects.get(pk=self.ride.id).status, Ride.RideStatus.ACCEPTED
        )

    def test_update_ride_status(self):
        request = self.factory.patch(
            f"/ride/{self.ride.id}/", {"status": Ride.RideStatus.STARTED}, format="json"
        )
        request.user = self.user
        view = RideModelViewSet.as_view({"patch": "partial_update"})
        response = view(request, pk=self.ride.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Ride.objects.get(pk=self.ride.id).status, Ride.RideStatus.STARTED
        )

    def test_list_all_rides(self):
        request = self.factory.get("/ride/")
        view = RideModelViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Ride.objects.count())
