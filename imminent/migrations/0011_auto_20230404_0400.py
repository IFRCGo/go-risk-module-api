# Generated by Django 3.2.17 on 2023-04-04 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imminent", "0010_adam_population_exposure"),
    ]

    operations = [
        migrations.AlterField(
            model_name="adam",
            name="hazard_type",
            field=models.CharField(
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
                verbose_name="Hazard type",
            ),
        ),
        migrations.AlterField(
            model_name="oddrin",
            name="hazard_type",
            field=models.CharField(
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
        migrations.AlterField(
            model_name="pdc",
            name="hazard_type",
            field=models.CharField(
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
        migrations.AlterField(
            model_name="pdcdisplacement",
            name="hazard_type",
            field=models.CharField(
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
    ]
