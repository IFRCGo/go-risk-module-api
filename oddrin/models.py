from django.db import models
from django.db.models.fields import TextField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class RiskFile(models.Model):
    file = models.FileField(
        upload_to='oddrin/', max_length=255,
        null=True, blank=True, verbose_name=_('file')
    )


class HazardType(models.TextChoices):
    EARTHQUAKE = 'EQ', 'Earthquake'
    FLOOD = 'FL', 'Flood'
    CYCLONE = 'TC', 'Cyclone'
    EPIDEMIC = 'EP', 'Epidemic'
    FOOD_INSECURITY = 'FI', 'Food Insecurity'
    STORM = 'SS', 'Storm Surge'
    DROUGHT = 'DR', 'Drought'
    TSUNAMI = 'TS', 'Tsunami'
    WIND = 'CD', 'Cyclonic Wind'


class Oddrin(models.Model):

    class FileType(models.TextChoices):
        RASTER = 'raster', 'Raster'
        VECTOR = 'vector', 'Vector'

    class DataSource(models.TextChoices):
        ODDRIN = 'oddrin', 'Oddrin'
        PACIFIC_DIASATER_CENTER = 'pdc', 'Pdc'

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        related_name='%(class)s_created',
        default=None, blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    modified_by = models.ForeignKey(
        User,
        related_name='%(class)s_modified',
        default=None, blank=True, null=True,
        on_delete=models.SET_NULL,
    )
    hazard_title = models.CharField(max_length=255, verbose_name=_('hazard title'))
    hazard_type = models.CharField(max_length=100, verbose_name=_('hazard type'), choices=HazardType.choices, blank=True)
    source_type = models.CharField(max_length=100, verbose_name=_('source type'), choices=DataSource.choices, blank=True)
    glide_number = models.CharField(max_length=100, verbose_name=_('glide number'), null=True, blank=True)
    uuid = models.CharField(max_length=128, verbose_name=_('uuid'), null=True, blank=True)
    latitude = models.FloatField(verbose_name=_('latitude'), null=True, blank=True)
    longitude = models.FloatField(verbose_name=_('longitude'), null=True, blank=True)
    iso3 = models.CharField(max_length=3, verbose_name=_('iso3'), null=True, blank=True)
    people_exposed = models.IntegerField(verbose_name=_('people exposed'), null=True, blank=True)
    people_displaced = models.IntegerField(verbose_name=_('people displaced'), null=True, blank=True)
    buildings_exposed = models.IntegerField(verbose_name=_('buildings exposed'), null=True, blank=True)
    lower_displacement = models.IntegerField(verbose_name=_('lower displacement'), null=True, blank=True)
    higher_displacement = models.IntegerField(verbose_name=_('higher displacement'), null=True, blank=True)
    file = models.FileField(
        verbose_name=_('file'),
        blank=True, null=True,
        upload_to='oddrin/files'
    )
    cog_file = models.FileField(
        verbose_name=_('cog file'),
        blank=True, null=True,
        upload_to='oddrin/cog_files'
    )
    file_type = models.CharField(max_length=100, verbose_name=_('file type'), choices=FileType.choices, blank=True)
    mapbox_layer_id = models.CharField(max_length=255, verbose_name=_('mapbox id'), null=True, blank=True)

    def str(self):
        return f'{self.hazard_title} - {self.hazard_type}'


class Idmc(models.Model):
    class ConfidenceType(models.TextChoices):
        HIGH = 'high', 'High'
        MEDIUM = 'medium', 'Medium'
        LOAD = 'low', 'Low'
        UNDEFINED = 'undefined', 'Undefined'

    country = models.CharField(max_length=255, verbose_name=_('country'))
    iso3 = models.CharField(max_length=3, verbose_name=_('iso3'), null=True, blank=True)
    hazard_type = models.CharField(
        max_length=100, verbose_name=_('hazard type'),
        choices=HazardType.choices,
        null=True, blank=True
    )
    confidence_type = models.CharField(
        max_length=100, verbose_name=_('confidence type'),
        choices=ConfidenceType.choices, blank=True
    )
    note = models.TextField(verbose_name=_('note'), blank=True, null=True)
    annual_average_displacement = models.FloatField(
        verbose_name=_('annual average displacement'), null=True, blank=True
    )
    january = models.FloatField(
        verbose_name=_('january'), null=True, blank=True
    )
    february = models.FloatField(
        verbose_name=_('february'), null=True, blank=True
    )
    march = models.FloatField(
        verbose_name=_('march'), null=True, blank=True
    )
    april = models.FloatField(
        verbose_name=_('april'), null=True, blank=True
    )
    may = models.FloatField(
        verbose_name=_('may'), null=True, blank=True
    )
    june = models.FloatField(
        verbose_name=_('june'), null=True, blank=True
    )
    july = models.FloatField(
        verbose_name=_('july'), null=True, blank=True
    )
    august = models.FloatField(
        verbose_name=_('august'), null=True, blank=True
    )
    september = models.FloatField(
        verbose_name=_('september'), null=True, blank=True
    )
    october = models.FloatField(
        verbose_name=_('october'), null=True, blank=True
    )
    november = models.FloatField(
        verbose_name=_('november'), null=True, blank=True
    )
    december = models.FloatField(
        verbose_name=_('december'), null=True, blank=True
    )

    def __str__(self):
        return f'{self.country} - {self.hazard_type}'


class DisplacementData(models.Model):

    country = models.ForeignKey('ipc.Country', on_delete=models.CASCADE)
    iso3 = models.CharField(max_length=3, verbose_name=_('iso3'), null=True, blank=True)
    hazard_type = models.CharField(
        max_length=100, verbose_name=_('hazard type'),
        choices=HazardType.choices,
        null=True, blank=True
    )
    note = models.TextField(verbose_name=_('note'), blank=True, null=True)
    annual_average_displacement = models.FloatField(
        verbose_name=_('annual average displacement'), null=True, blank=True
    )
    january = models.FloatField(
        verbose_name=_('january'), null=True, blank=True
    )
    february = models.FloatField(
        verbose_name=_('february'), null=True, blank=True
    )
    march = models.FloatField(
        verbose_name=_('march'), null=True, blank=True
    )
    april = models.FloatField(
        verbose_name=_('april'), null=True, blank=True
    )
    may = models.FloatField(
        verbose_name=_('may'), null=True, blank=True
    )
    june = models.FloatField(
        verbose_name=_('june'), null=True, blank=True
    )
    july = models.FloatField(
        verbose_name=_('july'), null=True, blank=True
    )
    august = models.FloatField(
        verbose_name=_('august'), null=True, blank=True
    )
    september = models.FloatField(
        verbose_name=_('september'), null=True, blank=True
    )
    october = models.FloatField(
        verbose_name=_('october'), null=True, blank=True
    )
    november = models.FloatField(
        verbose_name=_('november'), null=True, blank=True
    )
    december = models.FloatField(
        verbose_name=_('december'), null=True, blank=True
    )

    def __str__(self):
        return f'{self.country} - {self.hazard_type}'


class InformRisk(models.Model):
    country = models.ForeignKey(
        'ipc.Country', on_delete=models.CASCADE,
        verbose_name=_('country'), null=True, blank=True
    )
    hazard_type = models.CharField(
        max_length=100, verbose_name=_('hazard type'),
        choices=HazardType.choices, blank=True
    )
    risk_score = models.FloatField(verbose_name=_('risk_score'), null=True, blank=True)

    def __str__(self):
        return f'{self.country.name} - {self.hazard_type}'


class InformRiskSeasonal(models.Model):
    country = models.ForeignKey(
        'ipc.Country', on_delete=models.CASCADE,
        verbose_name=_('country'), null=True, blank=True
    )
    hazard_type = models.CharField(
        max_length=100, verbose_name=_('hazard type'),
        choices=HazardType.choices, blank=True
    )
    january = models.FloatField(
        verbose_name=_('january'), null=True, blank=True
    )
    february = models.FloatField(
        verbose_name=_('february'), null=True, blank=True
    )
    march = models.FloatField(
        verbose_name=_('march'), null=True, blank=True
    )
    april = models.FloatField(
        verbose_name=_('april'), null=True, blank=True
    )
    may = models.FloatField(
        verbose_name=_('may'), null=True, blank=True
    )
    june = models.FloatField(
        verbose_name=_('june'), null=True, blank=True
    )
    july = models.FloatField(
        verbose_name=_('july'), null=True, blank=True
    )
    august = models.FloatField(
        verbose_name=_('august'), null=True, blank=True
    )
    september = models.FloatField(
        verbose_name=_('september'), null=True, blank=True
    )
    october = models.FloatField(
        verbose_name=_('october'), null=True, blank=True
    )
    november = models.FloatField(
        verbose_name=_('november'), null=True, blank=True
    )
    december = models.FloatField(
        verbose_name=_('december'), null=True, blank=True
    )

    def __str__(self):
        return f'{self.country.name} - {self.hazard_type}'


class IdmcSuddenOnset(models.Model):
    country = models.ForeignKey(
        'ipc.Country', on_delete=models.CASCADE,
        verbose_name=_('country'), null=True, blank=True
    )
    hazard_type = models.CharField(
        max_length=100, verbose_name=_('hazard type'),
        choices=HazardType.choices, blank=True
    )
    annual_average_displacement = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('annual average displacement')
    )
    return_period_20_years = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('return period 20 years')
    )
    return_period_50_years = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('return period 50 years')
    )
    return_period_100_years = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('return period 100 years')
    )
    return_period_250_years = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('return period 250 years')
    )
    return_period_1000_years = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('return period 1000 years')
    )
    return_period_1500_years = models.IntegerField(
        null=True, blank=True,
        verbose_name=_('return period 1500 years')
    )

    def __str__(self):
        return f'{self.country} - {self.hazard_type}'


class GarHazard(models.Model):
    country = models.ForeignKey(
        'ipc.Country', on_delete=models.CASCADE,
        verbose_name=_('country'), null=True, blank=True
    )
    hazard_type = models.CharField(
        max_length=100, verbose_name=_('hazard type'),
        choices=HazardType.choices, blank=True
    )
    return_period_20_years = models.FloatField(
        null=True, blank=True,
        verbose_name=_('return period 20 years')
    )
    return_period_50_years = models.FloatField(
        null=True, blank=True,
        verbose_name=_('return period 50 years')
    )
    return_period_100_years = models.FloatField(
        null=True, blank=True,
        verbose_name=_('return period 100 years')
    )
    return_period_250_years = models.FloatField(
        null=True, blank=True,
        verbose_name=_('return period 250 years')
    )
    return_period_500_years = models.FloatField(
        null=True, blank=True,
        verbose_name=_('return period 500 years')
    )

    def __str__(self):
        return f'{self.country} - {self.hazard_type}'


class Pdc(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'A', 'Active',
        EXPIRED = 'E', 'Expired',

    created_at = models.DateTimeField(auto_now_add=True)
    hazard_id = models.CharField(verbose_name=_('hazard id'), max_length=255)
    hazard_name = models.CharField(verbose_name=_('hazard name'), max_length=255)
    hazard_type = models.CharField(
        max_length=100, verbose_name=_('hazard type'),
        choices=HazardType.choices, blank=True
    )
    latitude = models.FloatField(
        null=True, blank=True,
        verbose_name=_('latitude')
    )
    status = models.CharField(
        verbose_name=_('status'), max_length=20,
        choices=Status.choices, blank=True
    )
    longitude = models.FloatField(
        null=True, blank=True,
        verbose_name=_('longitude')
    )
    uuid = models.UUIDField(
        verbose_name=_('uuid'),
        null=True, blank=True,
    )
    description = models.TextField(
        verbose_name=_('description'),
        blank=True
    )
    start_date = models.DateField(
        null=True, blank=True,
        verbose_name=_('start date')
    )
    end_date = models.DateField(
        null=True, blank=True,
        verbose_name=_('end_date')
    )
    features = models.JSONField(
        blank=True, null=True,
        default=None,
        verbose_name=_('features')
    )

    def __str__(self):
        return f'{self.hazard_id} - {self.hazard_name}'


class PdcDisplacement(models.Model):
    hazard_type = models.CharField(
        max_length=100, verbose_name=_('hazard type'),
        choices=HazardType.choices, blank=True
    )
    country = models.ForeignKey(
        'ipc.Country', on_delete=models.CASCADE,
        verbose_name=_('country'), null=True, blank=True
    )
    pdc = models.ForeignKey(
        Pdc, on_delete=models.CASCADE,
        verbose_name=_('pdc')
    )
    population_exposure = models.JSONField(
        null=True, blank=True,
        default=None,
        verbose_name=_('population exposure')
    )
    capital_exposure = models.JSONField(
        null=True, blank=True,
        default=None,
        verbose_name=_('capital exposure')
    )

    def __str__(self):
        return f'{self.country.name} - {self.hazard_type}'
