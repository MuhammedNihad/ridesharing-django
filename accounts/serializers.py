from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model data.

    Attributes:
    model (Model): The User model.
    fields (list): The fields to include in the serialized data.
    """

    class Meta:
        model = User
        fields = ["id", "email", "name"]
