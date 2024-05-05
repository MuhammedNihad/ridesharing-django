import uuid

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import CustomUser

User = get_user_model()


class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "name": "Test User",
            "is_driver": True,
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        self.assertTrue(isinstance(self.user, CustomUser))
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertEqual(self.user.name, self.user_data["name"])
        self.assertTrue(self.user.is_driver)

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), self.user.email)

    def test_user_manager(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(User.objects.filter(is_driver=True).count(), 1)
        self.assertEqual(User.drivers.count(), 1)

    def test_custom_fields(self):
        # Check that the ID field is a valid UUID
        self.assertTrue(uuid.UUID(str(self.user.id), version=4))
        # Check that the ID field is a primary key
        self.assertEqual(self.user._meta.pk.name, "id")
        self.assertEqual(self.user.USERNAME_FIELD, "email")
        self.assertEqual(self.user.REQUIRED_FIELDS, [])
