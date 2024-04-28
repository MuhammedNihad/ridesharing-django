from django.contrib.auth import get_user_model
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import UserSerializer

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

