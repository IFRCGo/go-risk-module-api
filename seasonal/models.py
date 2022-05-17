from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.models import HazardType, Country


class Idmc(models.Model):
    class ConfidenceType(models.TextChoices):
        HIGH = 'high', 'High'
        MEDIUM = 'medium', 'Medium'
        LOAD = 'low', 'Low'
        UNDEFINED = 'undefined', 'Undefined'

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        verbose_name=_('country'), null=True, blank=True
    )
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

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
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
        Country, on_delete=models.CASCADE,
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
        Country, on_delete=models.CASCADE,
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
        Country, on_delete=models.CASCADE,
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
        Country, on_delete=models.CASCADE,
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
    return_period_25_years = models.FloatField(
        null=True, blank=True,
        verbose_name=_('return period 25 years')
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


class GarHazardDisplacement(models.Model):
    """
    This model displays both the economic loss and population exposure
    """

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        verbose_name=_('country'), null=True, blank=True
    )
    hazard_type = models.CharField(
        max_length=100, verbose_name=_('hazard type'),
        choices=HazardType.choices, blank=True
    )
    ten_years = models.JSONField(
        blank=True, null=True,
        default=dict,
        verbose_name=_('Ten years'),
    )
    twenty_years = models.JSONField(
        blank=True, null=True,
        default=dict,
        verbose_name=_('Twenty years'),
    )
    twenty_five_years = models.JSONField(
        blank=True, null=True,
        default=dict,
        verbose_name=_('Twenty five years'),
    )
    fifty_years = models.JSONField(
        blank=True, null=True,
        default=dict,
        verbose_name=_('Fifty years'),
    )
    hundred_years = models.JSONField(
        blank=True, null=True,
        default=dict,
        verbose_name=_('Hundred years'),
    )
    two_hundred_fifty_years = models.JSONField(
        blank=True, null=True,
        default=dict,
        verbose_name=_('Two Hundred Fifty years'),
    )
    five_hundred_years = models.JSONField(
        blank=True, null=True,
        default=dict,
        verbose_name=_('Five Hundred years'),
    )
    one_thousand_years = models.JSONField(
        blank=True, null=True,
        default=dict,
        verbose_name=_('One Thousand years')
    )
    one_thousand_five_hundred_years = models.JSONField(
        blank=True, null=True,
        default=dict,
        verbose_name=_('One Thousand Five hundred years')
    )


class GarProbabilistic(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        verbose_name=_('country'), null=True, blank=True
    )
    hazard_type = models.CharField(
        max_length=100, verbose_name=_('hazard type'),
        choices=HazardType.choices, blank=True
    )
    absolute_loss_in_million = models.FloatField(
        verbose_name=_('Absolute loss in Million'),
        null=True, blank=True
    )
    capital_stock_percentage = models.FloatField(
        verbose_name=_('Capital stock percentage'),
        null=True, blank=True

    )
    gfcf = models.FloatField(
        verbose_name=_('GFCF'),
        null=True, blank=True
    )
    social_exp = models.FloatField(
        verbose_name=_('Social Exp'),
        null=True, blank=True
    )
    total_revenue = models.FloatField(
        verbose_name=_('Total Revenue'),
        null=True, blank=True
    )
    gross_saving = models.FloatField(
        verbose_name=_('Gross Saving'),
        null=True, blank=True
    )

    def __str__(self):
        return f'{self.country.name} - {self.hazard_type}'


class Ipc(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'), null=True, blank=True)
    analysis_date = models.DateField(verbose_name=_('analysis date'), blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name=_('country'),
        null=True, blank=True
    )
    phase_population = models.IntegerField(verbose_name=_('phase population'))
    projected_phase_population = models.IntegerField(verbose_name=_('projected phase population'), null=True)
    census_population = models.IntegerField(verbose_name=_('census population'))
    current_period_start_date = models.DateField(verbose_name=_('current period start date'), blank=True, null=True)
    current_period_end_date = models.DateField(verbose_name=_('current period end date'), blank=True, null=True)
    projected_period_start_date = models.DateField(verbose_name=_('projected period start date'), blank=True, null=True)
    projected_period_end_date = models.DateField(verbose_name=_('projected period end date'), blank=True, null=True)
    second_projected_period_start_date = models.DateField(verbose_name=_('second projected period start date'), blank=True, null=True)
    second_projected_period_end_date = models.DateField(verbose_name=_('second projected period end date'), blank=True, null=True)
    hazard_type = models.CharField(max_length=100, verbose_name=_('hazard type'), choices=HazardType.choices, blank=True)
    is_projected = models.BooleanField(verbose_name=_('is projected'), default=False)

    def __str__(self):
        return f'{self.title} - {self.country}'


class EstimationType(models.TextChoices):
    CURRENT = 'current', 'Current'
    FIRST_PROJECTION = 'first_projection', 'First Projection'
    SECOND_PROJECTION = 'second_projection', 'Second Projection'


class IpcMonthly(models.Model):
    analysis_date = models.DateField(verbose_name=_('analysis date'), blank=True, null=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, verbose_name=_('country'),
        null=True, blank=True
    )
    phase_population = models.IntegerField(verbose_name=_('phase population'), null=True)
    projected_phase_population = models.IntegerField(verbose_name=_('projected phase population'), null=True)
    census_population = models.IntegerField(verbose_name=_('census population'))
    hazard_type = models.CharField(max_length=100, verbose_name=_('hazard type'), choices=HazardType.choices, blank=True)
    year = models.IntegerField(verbose_name=_('year'))
    month = models.IntegerField(verbose_name=_('month'))
    estimation_type = models.CharField(max_length=100, verbose_name=_('estimation type'), choices=EstimationType.choices, blank=True)

    def __str__(self):
        return f'{self.analysis_date} - {self.country.name}'


class GlobalDisplacement(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=_('country'))
    hazard_type = models.CharField(max_length=100, verbose_name=_('hazard type'), choices=HazardType.choices, blank=True)
    total_displacement = models.IntegerField(verbose_name=_('total displacement'), null=True, blank=True)
    year = models.IntegerField(verbose_name=_('year'))
    month = models.IntegerField(verbose_name=_('month'))
    analysis_date = models.DateField(verbose_name=_('analysis date'), blank=True, null=True)
    estimation_type = models.CharField(max_length=100, verbose_name=_('estimation type'), choices=EstimationType.choices, blank=True)

    def __str__(self):
        return f'{self.country} - {self.hazard_type} - {self.total_displacement}'


class ThinkHazardCountry(models.Model):
    country_id = models.CharField(max_length=255, verbose_name=_('country'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    iso3 = models.CharField(max_length=3, verbose_name=_('iso3'), null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.country_id}'


class ThinkHazardInformation(models.Model):
    class ThinkHazardLevel(models.TextChoices):
        LOW = 'low', 'Low'
        VERY_LOW = 'very low', 'Very Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    hazard_level = models.CharField(max_length=100, verbose_name=_('hazard level'),
                                    choices=ThinkHazardLevel.choices)
    information = models.TextField(verbose_name=_('information'))
    hazard_type = models.CharField(max_length=100, verbose_name=_('hazard type'), choices=HazardType.choices, blank=True)

    def __str__(self):
        return f'{self.hazard_type} {self.country.name}'
