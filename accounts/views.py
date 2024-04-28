from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .serializers import UserRegisterSerializer, UserSerializer

User = get_user_model()


class UserListReadOnlyViewset(ReadOnlyModelViewSet):
    """
    A read-only viewset for listing users excluding superusers.

    Attributes:
    queryset (QuerySet): The queryset of users excluding superusers.
    serializer_class (Serializer): The serializer class for user data.
    """

    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer


class UserSignupViewSet(GenericViewSet):
    """
    ViewSet for user signup.

    Attributes:
    queryset (QuerySet): Empty queryset required for ViewSet.
    serializer_class (Serializer): The serializer class for user registration.
    permission_classes (list): List of permission classes for this view.
    """

    queryset = User.objects.none()  # Required for ViewSet
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User signed up successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
