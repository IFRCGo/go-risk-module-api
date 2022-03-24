# Generated by Django 3.2.12 on 2022-03-24 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imminent', '0003_auto_20220321_0839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdc',
            name='features',
        ),
        migrations.AddField(
            model_name='pdc',
            name='footprint_geojson',
            field=models.JSONField(blank=True, default=None, null=True, verbose_name='Footprint Geojson'),
        ),
        migrations.AddField(
            model_name='pdc',
            name='storm_position_geojson',
            field=models.JSONField(blank=True, default=None, null=True, verbose_name='Storm Position Geojson'),
        ),
    ]
