from django.contrib import admin

from .models import Ride


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Ride model.

    Attributes:
    list_display (tuple): Fields displayed in the admin list view.
    list_filter (tuple): Filters available in the admin list view.
    date_hierarchy (str): Hierarchical date navigation in the admin list view.
    ordering (tuple): Default ordering for the admin list view.
    """

    list_display = ("id", "rider", "driver", "status", "created_at", "updated_at")
    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    class Meta:
        model = Ride
