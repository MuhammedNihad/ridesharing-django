# Generated by Django 5.0.4 on 2024-04-28 16:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_driver",
            field=models.BooleanField(
                default=False,
                help_text="Designates whether the user is driver or not",
                verbose_name="Driver status",
            ),
        ),
    ]
