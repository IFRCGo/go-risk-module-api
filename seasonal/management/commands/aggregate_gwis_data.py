import logging
import pandas as pd
import numpy as np

from django.core.management.base import BaseCommand

from seasonal.models import GwisSeasonal
from common.models import HazardType, Country
from imminent.models import GWIS


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Aggregate gwis data"

    def handle(self, *args, **options):

        # Define a mapping for month names
        month_mapping = {
            1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may',
            6: 'june', 7: 'july', 8: 'august', 9: 'september', 10: 'october',
            11: 'november', 12: 'december'
        }
        gwis_queryset = GWIS.objects.filter(dsr_type=GWIS.DSRTYPE.MONTHLY)
        gwis_values = gwis_queryset.values('country__name', 'month', 'dsr_avg', 'year')
        gwis_df = pd.DataFrame(list(gwis_values))
        gwis_df = gwis_df.rename(columns={'country__name': 'country'})
        gwis_df['month'] = gwis_df['month'].astype(int).map(month_mapping)
        new_df = gwis_df.groupby(['country', 'month'])['dsr_avg'].mean().reset_index()
        # new_df['dsr_avg'] = new_df['dsr_avg'].where(new_df['dsr_avg'].notnull(), None)
        gwises = []
        new_df = new_df.replace(np.nan, None)
        country_groups = new_df.groupby('country')
        for country_name, group in country_groups:
            gwis_data = {'country': Country.objects.filter(name__icontains=country_name).first()}
            for month in month_mapping.values():
                gwis_data[month] = (
                    group.loc[group['month'] == month, 'dsr_avg'].values[0]
                    if month in group['month'].values
                    else None
                )
            # group['dsr_avg'] = group['dsr_avg'].replace({np.NaN: None}, inplace=True)
            gwis_data['yearly_sum'] = group['dsr_avg'].sum()
            gwis_data['hazard_type'] = HazardType.WILDFIRE
            gwise = GwisSeasonal(**gwis_data)
            gwises.append(gwise)
        GwisSeasonal.objects.bulk_create(gwises)
