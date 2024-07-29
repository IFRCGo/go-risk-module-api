# Generated by Django 3.2.11 on 2022-02-03 05:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Region",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("region_id", models.IntegerField(verbose_name="region id")),
                ("region_name", models.CharField(max_length=255, verbose_name="region name")),
            ],
        ),
        migrations.AlterField(
            model_name="country",
            name="iso",
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name="iso2"),
        ),
        migrations.AddField(
            model_name="country",
            name="region",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="common.region", verbose_name="region"
            ),
        ),
    ]
