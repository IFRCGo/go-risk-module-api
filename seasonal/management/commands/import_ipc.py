import datetime
import logging
import requests

from django.core.management.base import BaseCommand

from seasonal.models import Ipc
from common.models import HazardType, Country


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import Ipc Data'

    def parse_date(self, date):
        if date:
            return datetime.datetime.strptime(date, '%b %Y').strftime('%Y-%m-01')

    def handle(self, *args, **options):
        for i in range(1, 9):
            ipc_url = f"http://mapipcissprd.us-east-1.elasticbeanstalk.com/api/public/population-tracking-tool/data/2017,2021/?page={i}&limit=200000&condition=A"
            response = requests.get(ipc_url)
            if response.status_code != 200:
                error_log = f'Error querying ipc data at {ipc_url}'
                logger.error(error_log)
                logger.error(response.content)
            ipc_data = response.json()
            for data in ipc_data:
                # Check whether is the country is present in local country
                if Country.objects.filter(name=data['country']).exists():
                    country = Country.objects.get(name=data['country'])
                    projected_period = data['analysis_period'].split('-')
                    if 'current_period_dates' in data:
                        current_period_dates = data['current_period_dates'].split('-')
                        if len(current_period_dates) == 2:
                            current_period_end_date = current_period_dates[1].strip()
                        else:
                            current_period_end_date = None
                        current_period_start_date = current_period_dates[0].strip()
                    else:
                        current_period_start_date = None
                        current_period_end_date = None
                    projected_period_start_date = projected_period[0].strip()
                    projected_period_end_date = projected_period[1].strip()
                    if 'phase6_P_population' in data:
                        projected_phase_population = data['phase6_P_population']
                    else:
                        projected_phase_population = None
                    data = {
                        'title': data['title'],
                        'country': country,
                        'analysis_date': self.parse_date(data['analysis_date']),
                        'phase_population': data['p3_plus_population'],
                        'projected_phase_population': projected_phase_population,
                        'census_population': data['census_population'],
                        'current_period_start_date': self.parse_date(current_period_start_date),
                        'current_period_end_date': self.parse_date(current_period_end_date),
                        'projected_period_start_date': self.parse_date(projected_period_start_date),
                        'projected_period_end_date': self.parse_date(projected_period_end_date),
                        'hazard_type': HazardType.FOOD_INSECURITY
                    }
                    Ipc.objects.create(**data)
