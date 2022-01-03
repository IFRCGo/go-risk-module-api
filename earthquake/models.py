from django.db import models
from django.utils.translation import ugettext_lazy as _

from ipc.models import Country


class Earthquake(models.Model):

    class MagnitudeType(models.TextChoices):
        TWO = '2', _('2')
        FOUR = '4', _('4')
        FA = 'fa', _('fa')
        H = 'H', _('H')
        LG = 'lg', _('lg')
        M = 'm', _('m')
        MA = 'ma', _('ma')
        mb = 'mb', _('mb')
        MBLG = 'MbLg', _('MbLg')
        MB_LG = 'Mb_lg', _('Mb_lg')
        MC = 'mc', _('mc')
        MD = 'md', _('md')
        MDL = 'mdl', _('mdl')
        ME = 'Me', _('Me')
        MFA = 'mfa', _('mfa')
        MH = 'mh', _('mh')
        MI = 'Mi',  _('Mi')
        MINT = 'mint', _('mint')
        ML = 'ml', _('ml')
        MLG = 'mlg', _('mlg')
        MLR = 'mlr', _('mlr')
        MLV = 'mlv', _('mlv')
        MS = 'Ms', _('Ms')
        MS_20 = 'ms_20', _('ms_20')
        MT = 'Mt', _('Mt')
        MUN = 'mun', _('mun')
        MW = 'mw', _('mw')
        MWB = 'mwb', _('mwb')
        MWC = 'mwc', _('mwc')
        MWP = 'mwp', _('mwp')
        MWR = 'mwr', _('mwr')
        MWW = 'mwm', _('mwm')
        NO = 'no', _('no')
        UK = 'uk', _('uk')
        UNKNOWN = 'Unknown', _('Unknown')

    event_id = models.CharField(max_length=100, verbose_name=_('event id'))
    event_title = models.CharField(max_length=255, verbose_name=_('event title'))
    event_place = models.CharField(max_length=255, verbose_name=_('event place'), null=True, blank=True)
    event_date = models.DateTimeField(
        verbose_name=_('event date'),
        null=True, blank=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('updated at'),
        null=True, blank=True
    )
    latitude = models.FloatField(verbose_name=_('latitude'))
    longitude = models.FloatField(verbose_name=_('longitude'))
    depth = models.FloatField(verbose_name=_('depth'))
    magnitude = models.FloatField(verbose_name=_('magnitude'))
    magnitude_type = models.CharField(max_length=20, choices=MagnitudeType.choices, verbose_name=_('magnitude type'))
    country = models.ForeignKey(
        Country,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('country')
    )

    def __str__(self):
        return f'{self.event_title} - {self.magnitude}'
