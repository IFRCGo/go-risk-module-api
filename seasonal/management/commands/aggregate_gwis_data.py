import datetime
import logging
import requests
import pandas as pd

from django.core.management.base import BaseCommand

from seasonal.models import GwisSeasonal
from common.models import HazardType, Country
from imminent.models import GWIS


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Aggregate gwis data"

    def handle(self, *args, **options):
        # fetch out all the qwis data
        # grouby the data by country
        # groupby month and exclude the month with null value
        # get the sum of monthy for each country
        gwis_df = pd.DataFrame(
            list(
                GWIS.objects.filter(
                    dsr_type=GWIS.DSRTYPE.MONTHLY,
                ).values(
                    'country__name',
                    'month',
                    'dsr_avg',
                    'year',
                )
            )
        )
        gwis_df = gwis_df.rename(columns={'country__name': 'country'})
        print(gwis_df)