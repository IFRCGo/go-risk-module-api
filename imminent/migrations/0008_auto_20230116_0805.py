# Generated by Django 3.2.16 on 2023-01-16 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imminent', '0007_adam_geojson'),
    ]

    operations = [
        migrations.AddField(
            model_name='adam',
            name='event_details',
            field=models.JSONField(blank=True, null=True, verbose_name='Event Details'),
        ),
        migrations.AlterField(
            model_name='adam',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Title'),
        ),
    ]
