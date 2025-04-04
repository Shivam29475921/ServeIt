# Generated by Django 5.1.8 on 2025-04-03 05:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a_rtchat", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="chatgroup",
            name="users_online",
            field=models.ManyToManyField(
                blank=True, related_name="online_in_groups", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
