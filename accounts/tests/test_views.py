from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class BaseViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()


class UserSignupViewSetTestCase(BaseViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.signup_url = "/signup/"

    def test_create_user(self):
        data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_invalid_data(self):
        data = {"email": "", "password": ""}
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class UserLoginViewSetTestCase(BaseViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.login_url = "/login/"
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )

    def test_login_user(self):
        data = {"email": "testuser@example.com", "password": "testpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user_invalid_data(self):
        data = {"email": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserListReadOnlyViewsetTestCase(BaseViewSetTestCase):
    def setUp(self):
        super().setUp()
        self.list_url = "/users/"
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.superuser = User.objects.create_superuser(
            email="testsuperuser@example.com", password="testsuperuserpassword"
        )

    def test_list_users(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], "testuser@example.com")

    def test_list_users_excludes_superusers(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        emails = [user["email"] for user in response.data]
        self.assertNotIn("testsuperuser@example.com", emails)
