# Generated by Django 3.2.17 on 2023-08-16 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_auto_20230206_0403'),
        ('imminent', '0018_gwis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meteoswissagg',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.country', verbose_name='country'),
        ),
    ]
