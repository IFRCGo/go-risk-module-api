# Generated by Django 3.2.11 on 2022-01-26 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ipc', '0011_auto_20211209_1003'),
        ('oddrin', '0019_garhazard_return_period_25_years'),
    ]

    operations = [
        migrations.CreateModel(
            name='GarHazardDisplacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hazard_type', models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind')], max_length=100, verbose_name='hazard type')),
                ('economic_loss_return_period_20_years', models.FloatField(blank=True, null=True, verbose_name='economic loss return period 20 years')),
                ('economic_loss_return_period_50_years', models.FloatField(blank=True, null=True, verbose_name='economic loss return period 50 years')),
                ('economic_loss_return_period_100_years', models.FloatField(blank=True, null=True, verbose_name='economic loss return period 100 years')),
                ('economic_loss_return_period_250_years', models.FloatField(blank=True, null=True, verbose_name='economic loss return period 250 years')),
                ('economic_loss_return_period_500_years', models.FloatField(blank=True, null=True, verbose_name='economic loss return period 500 years')),
                ('population_exposure_return_period_25_years', models.FloatField(blank=True, null=True, verbose_name='population exposure return period 25 years')),
                ('population_exposure_return_period_50_years', models.FloatField(blank=True, null=True, verbose_name='population exposure return period 50 years')),
                ('population_exposure_return_period_100_years', models.FloatField(blank=True, null=True, verbose_name='population exposure return period 100 years')),
                ('population_exposure_return_period_200_years', models.FloatField(blank=True, null=True, verbose_name='population exposure return period 250 years')),
                ('population_exposure_return_period_500_years', models.FloatField(blank=True, null=True, verbose_name='population exposure return period 500 years')),
                ('population_exposure_return_period_1000_years', models.FloatField(blank=True, null=True, verbose_name='population exposure return period 1000 years')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ipc.country', verbose_name='country')),
            ],
        ),
    ]