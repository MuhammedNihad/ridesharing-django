from rest_framework.serializers import ModelSerializer

from .models import Ride


class RideSerializer(ModelSerializer):
    """
    Serializer for the Ride model with full details.

    Attributes:
    model (Model): The Ride model.
    fields (list): Fields to include in the serialized data.
    """

    class Meta:
        model = Ride
        fields = [
            "id",
            "url",
            "rider",
            "driver",
            "status",
            "pickup_location",
            "dropoff_location",
            "created_at",
            "updated_at",
        ]


class RideCreateSerializer(ModelSerializer):
    """
    Serializer for creating new Ride instances.

    Attributes:
    model (Model): The Ride model.
    fields (list): Fields required for creating new Ride instances.
    """

    class Meta:
        model = Ride
        fields = ["pickup_location", "dropoff_location"]


class RideStatusUpdateSerializer(ModelSerializer):
    """
    Serializer for updating the status of Ride instances.

    Attributes:
    model (Model): The Ride model.
    fields (list): Fields required for updating the status of Ride instances.
    """

    class Meta:
        model = Ride
        fields = ["url", "status"]
