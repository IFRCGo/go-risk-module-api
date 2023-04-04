# Generated by Django 3.2.17 on 2023-04-04 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seasonal', '0015_auto_20221214_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='displacementdata',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, null=True, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='garhazard',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='garhazarddisplacement',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='garprobabilistic',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='globaldisplacement',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='idmc',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, null=True, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='idmcsuddenonset',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='informrisk',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='informriskseasonal',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='ipc',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='ipcmonthly',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='possibleearlyactions',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='riskscore',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, verbose_name='hazard type'),
        ),
        migrations.AlterField(
            model_name='thinkhazardinformation',
            name='hazard_type',
            field=models.CharField(blank=True, choices=[('EQ', 'Earthquake'), ('FL', 'Flood'), ('TC', 'Cyclone'), ('EP', 'Epidemic'), ('FI', 'Food Insecurity'), ('SS', 'Storm Surge'), ('DR', 'Drought'), ('TS', 'Tsunami'), ('CD', 'Cyclonic Wind'), ('WF', 'WildFire')], max_length=100, verbose_name='hazard type'),
        ),
    ]
