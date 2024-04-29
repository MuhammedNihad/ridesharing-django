# Generated by Django 5.0.4 on 2024-04-28 17:49

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ride",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("pickup_location", models.URLField(verbose_name="Pickup location")),
                ("dropoff_location", models.URLField(verbose_name="Dropoff location")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("not_started", "Not Started"),
                            ("started", "Started"),
                            ("requested", "Requested"),
                            ("accepted", "Accepted"),
                            ("completed", "Completed"),
                            ("cancelled ", "Cancelled"),
                        ],
                        default="not_started",
                        max_length=20,
                        verbose_name="Ride status",
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        limit_choices_to={"is_driver": True, "is_superuser": False},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rides_as_driver",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "rider",
                    models.ForeignKey(
                        limit_choices_to={"is_driver": False, "is_superuser": False},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rides_as_rider",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]