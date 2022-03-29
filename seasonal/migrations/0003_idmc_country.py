# Generated by Django 3.2.11 on 2022-02-07 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20220203_0523'),
        ('seasonal', '0002_remove_idmc_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='idmc',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.country', verbose_name='country'),
        ),
    ]