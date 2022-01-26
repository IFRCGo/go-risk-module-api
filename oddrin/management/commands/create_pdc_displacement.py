import os
import requests
import logging

from django.core.management.base import BaseCommand

from oddrin.models import Pdc, PdcDisplacement
from ipc.models import Country


logger = logging.getLogger()


class Command(BaseCommand):
    help = 'Import Hazard Exposure Data'

    def handle(self, *args, **options):
        uuids = Pdc.objects.values_list('uuid', 'hazard_type')
        for uuid, hazard_type in uuids:
            access_token = os.environ.get('PDC_ACCESS_TOKEN')
            url = f'https://sentry.pdc.org/hp_srv/services/hazard/{uuid}/exposure/latest/'
            headers = {'Authorization': "Bearer {}".format(access_token)}
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                error_log = f'Error querying PDC Exposure data at {url}'
                logger.error(error_log)
                logger.error(response.content)
            response_data = response.json()
            for key, value in response_data.items():
                if 'totalByCountry' in key:
                    data = response_data['totalByCountry']
                    if len(data) > 0:
                        for d in data:
                            if Country.objects.filter(iso3=d['country'].lower()).exists():
                                c_data = {
                                    'country': Country.objects.filter(iso3=d['country'].lower()).first(),
                                    'hazard_type': hazard_type,
                                    'population_exposure': d['population'],
                                    'capital_exposure': d['capital'],
                                    'pdc': Pdc.objects.get(uuid=uuid).first(),
                                }
                                PdcDisplacement.objects.get_or_create(**c_data)
