# Generated by Django 3.2.12 on 2022-02-18 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0002_auto_20220203_0523"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="region",
            name="region_id",
        ),
        migrations.RemoveField(
            model_name="region",
            name="region_name",
        ),
    ]
