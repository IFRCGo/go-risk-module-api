# Generated by Django 3.2.16 on 2023-01-30 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imminent", "0008_auto_20230116_0805"),
    ]

    operations = [
        migrations.AddField(
            model_name="adam",
            name="storm_position_geojson",
            field=models.JSONField(blank=True, null=True, verbose_name="Storm Position"),
        ),
    ]
