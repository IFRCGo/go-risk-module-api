# Generated by Django 3.2.12 on 2022-02-18 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20220218_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='name',
            field=models.IntegerField(choices=[(0, 'Africa'), (1, 'Americas'), (2, 'Asia Pacific'), (3, 'Europe'), (4, 'Middle East & North Africa')], default=1, verbose_name='name'),
            preserve_default=False,
        ),
    ]
