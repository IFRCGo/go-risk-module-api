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


class PossibleEarlyActionsSectors(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('name')
    )


class PossibleEarlyActions(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE,
        verbose_name=_('country')
    )
    hazard_type = models.CharField(
        max_length=100, verbose_name=_('hazard type'),
        choices=HazardType.choices, blank=True
    )
    early_actions = models.TextField(
        verbose_name=_('Possible Early Actions'),
        null=True, blank=True
    )
    hazard_name = models.CharField(
        max_length=255, verbose_name=_('Hazard Name'),
        null=True, blank=True
    )
    location = models.TextField(
        verbose_name=_('Location Description'),
        null=True, blank=True
    )
    sectors = models.ManyToManyField(
        PossibleEarlyActionsSectors,
        verbose_name=_('Sectors'),
        blank=True
    )
    intended_purpose = models.TextField(
        verbose_name=_('Intended Purpose'),
        null=True, blank=True
    )
    organization = models.CharField(
        verbose_name=_('Organization'), max_length=255,
        null=True, blank=True
    )
    budget = models.IntegerField(
        verbose_name=_('Budget'),
        null=True, blank=True
    )
    cost = models.IntegerField(
        verbose_name=_('Cost'),
        null=True, blank=True
    )
    implementation_date = models.DateField(
        verbose_name=_('Implementation Date'),
        null=True, blank=True
    )
    implementation_date_raw = models.CharField(
        max_length=255, verbose_name=_('Implementation Date Raw'),
        null=True, blank=True
    )
    timeframe = models.IntegerField(
        verbose_name=_('Timeframe'),
        null=True, blank=True
    )
    timeframe_raw = models.CharField(
        max_length=255, verbose_name=_('Timeframe Raw'),
        null=True, blank=True
    )
    effective_time = models.IntegerField(
        verbose_name=_('Effective Time'),
        null=True, blank=True
    )
    effective_time_raw = models.CharField(
        max_length=255, verbose_name=_('Effective Time Raw'),
        null=True, blank=True
    )
    number_of_people_covered = models.IntegerField(
        verbose_name=_('Number of People Covered'),
        null=True, blank=True
    )
    number_of_people_at_risk = models.IntegerField(
        verbose_name=_('Number of people At Risk'),
        null=True, blank=True
    )
    scalability = models.CharField(
        verbose_name=_('Scalability'),
        null=True, blank=True,
        max_length=255
    )
    cross_cutting = models.TextField(
        verbose_name=_('Cross Cutting'),
        null=True, blank=True
    )
    resources_used = models.TextField(
        verbose_name=_('Resources Used'),
        null=True, blank=True
    )
    impact_action = models.TextField(
        verbose_name=_('Impact Action'),
        null=True, blank=True
    )
    evidence_of_sucess = models.TextField(
        verbose_name=_('Evidence of Sucess'),
        null=True, blank=True
    )
    resource = models.TextField(
        verbose_name=_('Resource'),
        null=True, blank=True
    )
    link_to_resources = models.CharField(
        verbose_name=_('Link To Resources'),
        null=True, blank=True,
        max_length=255
    )
    exist_in_hub = models.BooleanField(
        verbose_name=_('Exist in Hub'),
        null=True, blank=True
    )

    def __str__(self):
        return f'{self.country.name} {self.hazard_type}'


class PublishReportProgram(models.Model):
    start_date = models.DateTimeField(
        verbose_name=_('Start Date'),
        null=True, blank=True
    )
    end_date = models.DateTimeField(
        verbose_name=_('End Date'),
        null=True, blank=True
    )
    inactive = models.BooleanField(
        verbose_name=_('Inactive'),
        null=True, blank=True
    )
    country = models.ForeignKey(
        Country,
        verbose_name=_('Country'),
        on_delete=models.CASCADE
    )
    program_name = models.CharField(
        max_length=255,
        verbose_name=_('Program Name')
    )
    program_manager = models.CharField(
        max_length=255,
        verbose_name=_('Program Manager')
    )
    area = models.CharField(
        max_length=255,
        verbose_name=_('Area'),
        null=True, blank=True
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True, blank=True
    )
    communities = models.TextField(
        verbose_name=_('Communities'),
        null=True, blank=True
    )
    bread_cumbs = models.TextField(
        verbose_name=_('Bread Cumbs'),
        null=True, blank=True
    )
    accuracy_level = models.CharField(
        verbose_name=_('Accuracy'),
        null=True, blank=True,
        max_length=255
    )
    community_engagement = models.TextField(
        verbose_name=_('Community Engagement'),
        null=True, blank=True
    )
    measurement_assignment = models.TextField(
        verbose_name=_('Measurement Assignment'),
        null=True, blank=True
    )
    community_vca = models.TextField(
        verbose_name=_('Community VCA'),
        null=True, blank=True
    )


class PublishReport(models.Model):
    program = models.ForeignKey(
        PublishReportProgram,
        verbose_name=_('Program Name'),
        on_delete=models.CASCADE
    )
    publish_report_id = models.CharField(
        verbose_name=_('Publish Report'),
        max_length=255,
        null=True, blank=True
    )
    report_name = models.CharField(
        verbose_name=_('Report Name'),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True, blank=True
    )
    email = models.CharField(
        verbose_name=_('Email'),
        null=True, blank=True,
        max_length=255
    )
    attachment_name = models.CharField(
        verbose_name=_('Attachment Name'),
        null=True, blank=True,
        max_length=255
    )
    attachment = models.CharField(
        verbose_name=_('Attachment'),
        null=True, blank=True,
        max_length=255
    )
    attachment_url = models.CharField(
        verbose_name=_('Attachment URL'),
        max_length=255,
        null=True, blank=True
    )

    def __str__(self):
        return f'{self.report_name} - {self.program.program_name} - {self.program.country.name}'


class RiskScore(models.Model):
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
    yearly_sum = models.FloatField(
        verbose_name=_('yearly_sum'), null=True, blank=True
    )

    def __str__(self):
        return f'{self.country.name} - {self.hazard_type} - {self.yearly_sum}'
