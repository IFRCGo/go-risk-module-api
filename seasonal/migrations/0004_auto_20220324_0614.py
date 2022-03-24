# Generated by Django 3.2.12 on 2022-03-24 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seasonal', '0003_idmc_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='garhazarddisplacement',
            name='economic_loss_return_period_100_years',
        ),
        migrations.RemoveField(
            model_name='garhazarddisplacement',
            name='economic_loss_return_period_20_years',
        ),
        migrations.RemoveField(
            model_name='garhazarddisplacement',
            name='economic_loss_return_period_250_years',
        ),
        migrations.RemoveField(
            model_name='garhazarddisplacement',
            name='economic_loss_return_period_500_years',
        ),
        migrations.RemoveField(
            model_name='garhazarddisplacement',
            name='economic_loss_return_period_50_years',
        ),
        migrations.RemoveField(
            model_name='garhazarddisplacement',
            name='population_exposure_return_period_1000_years',
        ),
        migrations.RemoveField(
            model_name='garhazarddisplacement',
            name='population_exposure_return_period_100_years',
        ),
        migrations.RemoveField(
            model_name='garhazarddisplacement',
            name='population_exposure_return_period_200_years',
        ),
        migrations.RemoveField(
            model_name='garhazarddisplacement',
            name='population_exposure_return_period_25_years',
        ),
        migrations.RemoveField(
            model_name='garhazarddisplacement',
            name='population_exposure_return_period_500_years',
        ),
        migrations.RemoveField(
            model_name='garhazarddisplacement',
            name='population_exposure_return_period_50_years',
        ),
        migrations.AddField(
            model_name='garhazarddisplacement',
            name='fifty_years',
            field=models.JSONField(blank=True, default=None, null=True, verbose_name='Fifty years'),
        ),
        migrations.AddField(
            model_name='garhazarddisplacement',
            name='five_hundred_years',
            field=models.JSONField(blank=True, default=None, null=True, verbose_name='Five Hundred years'),
        ),
        migrations.AddField(
            model_name='garhazarddisplacement',
            name='hundred_years',
            field=models.JSONField(blank=True, default=None, null=True, verbose_name='Hundred years'),
        ),
        migrations.AddField(
            model_name='garhazarddisplacement',
            name='one_thousand_years',
            field=models.JSONField(blank=True, default=None, null=True, verbose_name='One Thousand years'),
        ),
        migrations.AddField(
            model_name='garhazarddisplacement',
            name='ten_years',
            field=models.JSONField(blank=True, default=None, null=True, verbose_name='Ten years'),
        ),
        migrations.AddField(
            model_name='garhazarddisplacement',
            name='twenty_five_years',
            field=models.JSONField(blank=True, default=None, null=True, verbose_name='Twenty five years'),
        ),
        migrations.AddField(
            model_name='garhazarddisplacement',
            name='twenty_years',
            field=models.JSONField(blank=True, default=None, null=True, verbose_name='Twenty years'),
        ),
        migrations.AddField(
            model_name='garhazarddisplacement',
            name='two_hundred_fifty_years',
            field=models.JSONField(blank=True, default=None, null=True, verbose_name='Two Hundred Fifty years'),
        ),
    ]
