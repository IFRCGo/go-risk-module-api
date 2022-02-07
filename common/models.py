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


class Region(models.Model):
    region_id = models.IntegerField(verbose_name=_('region id'))
    region_name = models.CharField(verbose_name=_('region name'), max_length=255)

    def __str__(self):
        return f'{self.region_id} - {self.region_name}'


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'), null=True, blank=True)
    iso3 = models.CharField(
        max_length=3, verbose_name=_('iso3'),
        null=True, blank=True
    )
    iso = models.CharField(
        max_length=2, verbose_name=_('iso2'),
        null=True, blank=True
    )
    region = models.ForeignKey(
        Region,
        verbose_name=_('region'),
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.name} - {self.iso3}'

    def save(self, *args, **kwargs):
        if self.iso3:
            self.iso3 = self.iso3.lower()
        if self.iso:
            self.iso = self.iso.lower()
        return super().save(*args, **kwargs)
