# Generated by Django 3.2.12 on 2022-03-25 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imminent', '0004_auto_20220324_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdc',
            name='severity',
            field=models.CharField(blank=True, choices=[('warning', 'Warning'), ('watch', 'Watch'), ('advisory', 'Advisory'), ('information', 'Information')], max_length=100, null=True, verbose_name='severity'),
        ),
    ]
