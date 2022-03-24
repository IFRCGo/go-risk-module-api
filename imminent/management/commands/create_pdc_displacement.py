import os
import requests
import logging

from django.core.management.base import BaseCommand

from imminent.models import Pdc, PdcDisplacement
from common.models import Country, HazardType


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
            for pdc in Pdc.objects.filter(uuid=uuid):
                data = response_data.get('totalByCountry')
                if data and len(data) > 0:
                    for d in data:
                        if Country.objects.filter(iso3=d['country'].lower()).exists():
                            c_data = {
                                'country': Country.objects.filter(iso3=d['country'].lower()).first(),
                                'hazard_type': hazard_type,
                                'population_exposure': d['population'],
                                'capital_exposure': d['capital'],
                                'pdc': pdc,
                            }
                            PdcDisplacement.objects.create(**c_data)
                else:
                    PdcDisplacement.objects.create(
                        hazard_type=hazard_type,
                        pdc=pdc
                    )
