# Generated by Django 5.0.1 on 2024-02-02 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menuitem",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="menu_items",
                to="LittleLemonAPI.category",
            ),
        ),
    ]
