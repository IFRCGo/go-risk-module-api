# Generated by Django 3.2.16 on 2022-12-14 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("seasonal", "0014_riskscore"),
    ]

    operations = [
        migrations.AddField(
            model_name="riskscore",
            name="lcc",
            field=models.FloatField(blank=True, null=True, verbose_name="llc"),
        ),
        migrations.AddField(
            model_name="riskscore",
            name="population_in_thousands",
            field=models.FloatField(blank=True, null=True, verbose_name="population_in_thousands"),
        ),
    ]
