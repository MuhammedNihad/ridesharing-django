from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Ride
from .serializers import (
    RideCreateSerializer,
    RideSerializer,
    RideStatusUpdateSerializer,
)


class RideModelViewSet(ModelViewSet):
    """
    ViewSet for handling CRUD operations on Ride instances.

    Attributes:
    queryset (QuerySet): The queryset containing all Ride instances.
    """

    queryset = Ride.objects.all()

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.

        Returns:
        Serializer: The serializer class to use.
        """
        if self.action == "create":
            return RideCreateSerializer
        elif self.action == "update":
            return RideStatusUpdateSerializer
        return RideSerializer

    def perform_create(self, serializer):
        """
        Perform additional actions during creation of a new Ride instance.

        Args:
        serializer (Serializer): The serializer instance used for creation.
        """
        # Set the rider and possibly other fields based on request data
        serializer.save(rider=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new Ride instance based on the request data.

        Args:
        request (Request): The HTTP request object.

        Returns:
        Response: HTTP response with details of the created Ride instance.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Customize the response here
        response_data = {
            "message": "Ride request created successfully!",
            "pickup_location": serializer.instance.pickup_location,
            "dropoff_location": serializer.instance.dropoff_location,
            "status": serializer.instance.status,
            "requested_at": serializer.instance.created_at,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
