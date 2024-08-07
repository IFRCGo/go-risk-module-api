# Generated by Django 3.2.17 on 2023-04-28 08:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0007_auto_20230206_0403"),
        ("imminent", "0014_meteoswiss"),
    ]

    operations = [
        migrations.CreateModel(
            name="MeteoSwissAgg",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("event_details", models.JSONField(blank=True, null=True, verbose_name="Event Details")),
                ("hazard_name", models.CharField(max_length=255, verbose_name="hazard name")),
                (
                    "hazard_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("EQ", "Earthquake"),
                            ("FL", "Flood"),
                            ("TC", "Cyclone"),
                            ("EP", "Epidemic"),
                            ("FI", "Food Insecurity"),
                            ("SS", "Storm Surge"),
                            ("DR", "Drought"),
                            ("TS", "Tsunami"),
                            ("CD", "Cyclonic Wind"),
                            ("WF", "WildFire"),
                        ],
                        max_length=100,
                        verbose_name="hazard type",
                    ),
                ),
                ("start_date", models.DateField(verbose_name="start date")),
                ("end_date", models.DateField(verbose_name="end date")),
                (
                    "country",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="common.country", verbose_name="country"),
                ),
            ],
        ),
    ]
