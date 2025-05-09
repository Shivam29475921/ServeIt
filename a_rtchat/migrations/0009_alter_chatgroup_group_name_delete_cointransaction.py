# Generated by Django 5.1.8 on 2025-04-04 16:25

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a_rtchat", "0008_alter_chatgroup_group_name_cointransaction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatgroup",
            name="group_name",
            field=models.CharField(
                default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True
            ),
        ),
        migrations.DeleteModel(
            name="CoinTransaction",
        ),
    ]
