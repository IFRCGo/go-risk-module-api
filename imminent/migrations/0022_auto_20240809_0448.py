# Generated by Django 3.2.17 on 2024-08-09 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imminent", "0021_auto_20230920_1421"),
    ]

    operations = [
        migrations.AddField(
            model_name="pdc",
            name="cyclone_five_days_cou",
            field=models.JSONField(blank=True, default=None, null=True, verbose_name="Cyclone Five Days Cone of Uncertainty"),
        ),
        migrations.AddField(
            model_name="pdc",
            name="cyclone_three_days_cou",
            field=models.JSONField(blank=True, default=None, null=True, verbose_name="Cyclone Three Days Cone of Uncertainty"),
        ),
    ]
