# Generated by Django 3.2.17 on 2023-05-16 04:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0007_auto_20230206_0403"),
        ("imminent", "0017_auto_20230503_0935"),
    ]

    operations = [
        migrations.CreateModel(
            name="GWIS",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("month", models.CharField(max_length=255, verbose_name="month")),
                ("dsr", models.FloatField(blank=True, null=True, verbose_name="dsr")),
                ("dsr_min", models.FloatField(blank=True, null=True, verbose_name="dsr min")),
                ("dsr_avg", models.FloatField(blank=True, null=True, verbose_name="dsr avg")),
                ("dsr_max", models.FloatField(blank=True, null=True, verbose_name="dsr max")),
                ("year", models.IntegerField(verbose_name="year")),
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
                (
                    "dsr_type",
                    models.CharField(
                        blank=True,
                        choices=[("monthly", "Monthly"), ("cumulative", "Cummulative")],
                        max_length=100,
                        verbose_name="dsr type",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="common.country", verbose_name="country"),
                ),
            ],
        ),
    ]
