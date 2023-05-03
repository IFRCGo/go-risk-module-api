# Generated by Django 3.2.17 on 2023-05-03 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imminent', '0016_meteoswissagg_geojson_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='meteoswissagg',
            name='latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='latitude'),
        ),
        migrations.AddField(
            model_name='meteoswissagg',
            name='longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='longitude'),
        ),
    ]
