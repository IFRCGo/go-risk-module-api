# Generated by Django 3.2.13 on 2022-05-18 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_country_bbox'),
        ('seasonal', '0008_garprobabilistic'),
    ]

    operations = [
        migrations.CreateModel(
            name='PossibleEarlyActions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hazard_type', models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind')], max_length=100, verbose_name='hazard type')),
                ('early_actions', models.TextField(blank=True, null=True, verbose_name='Possible Early Actions')),
                ('hazard_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Hazard Name')),
                ('location', models.TextField(blank=True, null=True, verbose_name='Location Description')),
                ('sector', models.CharField(blank=True, max_length=255, null=True, verbose_name='Sector')),
                ('intended_purpose', models.TextField(blank=True, null=True, verbose_name='Intended Purpose')),
                ('organization', models.CharField(blank=True, max_length=255, null=True, verbose_name='Organization')),
                ('budget', models.IntegerField(blank=True, null=True, verbose_name='Budget')),
                ('cost', models.IntegerField(blank=True, null=True, verbose_name='Cost')),
                ('implementation_date', models.DateField(blank=True, null=True, verbose_name='Implementation Date')),
                ('timeframe', models.IntegerField(blank=True, null=True, verbose_name='Timeframe')),
                ('effective_time', models.IntegerField(blank=True, null=True, verbose_name='Effective Time')),
                ('number_of_people_covered', models.IntegerField(blank=True, null=True, verbose_name='Number of People Covered')),
                ('number_of_people_at_risk', models.IntegerField(blank=True, null=True, verbose_name='Number of people At Risk')),
                ('scalability', models.CharField(blank=True, max_length=255, null=True, verbose_name='Scalability')),
                ('cross_cutting', models.TextField(blank=True, null=True, verbose_name='Cross Cutting')),
                ('resources_used', models.TextField(blank=True, null=True, verbose_name='Resources Used')),
                ('impact_action', models.TextField(blank=True, null=True, verbose_name='Impact Action')),
                ('evidence_of_sucess', models.TextField(blank=True, null=True, verbose_name='Evidence of Sucess')),
                ('resource', models.TextField(blank=True, null=True, verbose_name='Resource')),
                ('link_to_resources', models.CharField(blank=True, max_length=255, null=True, verbose_name='Link To Resources')),
                ('exist_in_hub', models.BooleanField(blank=True, null=True, verbose_name='Exist in Hub')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.country', verbose_name='country')),
            ],
        ),
    ]
