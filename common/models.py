from django.db import models
from django.utils.translation import ugettext_lazy as _


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
    WILDFIRE = 'WF', 'WildFire'


class Region(models.Model):
    class RegionName(models.IntegerChoices):
        AFRICA = 0, _('Africa')
        AMERICAS = 1, _('Americas')
        ASIA_PACIFIC = 2, _('Asia Pacific')
        EUROPE = 3, _('Europe')
        MENA = 4, _('Middle East & North Africa')

    name = models.IntegerField(verbose_name=_('name'), choices=RegionName.choices,)

    def __str__(self):
        return f'{self.name}'


class Country(models.Model):
    class CountryType(models.IntegerChoices):
        '''
            We use the Country model for some things that are not "Countries". This helps classify the type.
        '''
        COUNTRY = 1, _('Country')
        CLUSTER = 2, _('Cluster')
        REGION = 3, _('Region')
        COUNTRY_OFFICE = 4, _('Country Office')
        REPRESENTATIVE_OFFICE = 5, _('Representative Office')

    name = models.CharField(max_length=255, verbose_name=_('name'), null=True, blank=True)
    iso3 = models.CharField(
        max_length=3, verbose_name=_('iso3'),
        null=True, blank=True
    )
    iso = models.CharField(
        max_length=2, verbose_name=_('iso2'),
        null=True, blank=True
    )
    record_type = models.IntegerField(
        choices=CountryType.choices,
        verbose_name=_('type'),
        null=True, blank=True,
        help_text=_('Type of entity')
    )
    region = models.ForeignKey(
        Region,
        verbose_name=_('region'),
        null=True, blank=True,
        on_delete=models.SET_NULL
    )
    bbox = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        verbose_name=_('bbox'),
    )
    centroid = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        verbose_name=_('centroid'),
    )
    independent = models.BooleanField(
        default=None, null=True,
        help_text=_('Is this an independent country?')
    )
    is_deprecated = models.BooleanField(
        default=False,
        help_text=_('Is this an active, valid country?')
    )

    def __str__(self):
        return f'{self.name} - {self.iso3}'

    def save(self, *args, **kwargs):
        if self.iso3:
            self.iso3 = self.iso3.lower()
        if self.iso:
            self.iso = self.iso.lower()
        return super().save(*args, **kwargs)
