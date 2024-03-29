# Generated by Django 5.0.1 on 2024-02-03 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0003_alter_orderitem_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_order",
                to="LittleLemonAPI.order",
            ),
        ),
    ]
