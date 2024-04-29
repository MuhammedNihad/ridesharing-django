from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from ..admin import RideAdmin
from ..models import Ride

User = get_user_model()


class RideAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email="testadmin@example.com", password="testpassword", is_superuser=True
        )
        self.client.force_login(self.user)

    def test_ride_admin_list_display(self):
        ride_admin = RideAdmin(Ride, self.site)
        self.assertEqual(
            ride_admin.list_display,
            ("id", "rider", "driver", "status", "created_at", "updated_at"),
        )

    def test_ride_admin_list_filter(self):
        ride_admin = RideAdmin(Ride, self.site)
        self.assertEqual(ride_admin.list_filter, ("status", "created_at", "updated_at"))

    def test_ride_admin_date_hierarchy(self):
        ride_admin = RideAdmin(Ride, self.site)
        self.assertEqual(ride_admin.date_hierarchy, "created_at")

    def test_ride_admin_ordering(self):
        ride_admin = RideAdmin(Ride, self.site)
        self.assertEqual(ride_admin.ordering, ("-created_at",))

    def test_ride_admin_view_list(self):
        request = self.factory.get("/admin/ride/ride/")
        request.user = self.user
        response = RideAdmin(Ride, self.site).changelist_view(request)
        self.assertEqual(response.status_code, 200)
