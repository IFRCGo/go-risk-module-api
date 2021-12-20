from django.db import models
from django.db.models.expressions import Value
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
            access_token = 'eyJraWQiOiIyMDE4LTA0LTA1fHRlc3RhcHBzLnBkYy5vcmciLCJhbGciOiJSUzUxMiJ9.eyJqdGkiOiJkNzM1MDk4NS1mMDZiLTQyZGUtYjhhYi1mMDg5ZGU3YmNhY2MiLCJpc3MiOiJodHRwczovL3Rlc3RhcHBzLnBkYy5vcmcvand0L2p3a3MuanNvbiIsImlhdCI6MTYzOTA5OTI3NywibmJmIjoxNjM5MDk5Mjc3LCJzdWIiOiJ0ZXN0YXBwcy5wZGMub3JnIiwiZXhwIjo0MTAyNDQ0ODAwLCJ1c2VyUm9sZXMiOlsiTE9HSU4iXSwidXNlckdyb3VwSWQiOiIyIiwidG9rZW5UeXBlIjoibG9uZyJ9.U4PEr83nLptbQ0OIKWhGGuokYN9FkfMociiBrYCe4v8j7yvG-1RzM-ETCqi8t7U-TTiIk9AA4bKAl72Tf30mtNC42etpga7wStOUpzHnmJ32WkYw9xocMQhJIuORz4aVDNjlyhsO2nyTGOpZWy4EFQVhUkw3Zx0Ka8K0HZ0JTN1kaQuAMg2JciL8Y1mKNKE9f0rWIg0UM80FF1Rt_R1x9HtioXzA3pVRZTOcgN5Fydv6NEaR8NonTaXigt1p_1NFuw3RuAJffqfgvgKnyi8aEUYo_Ec6J_i3vSmJrcX2_kV0H7L-vzJK1mHl-lZNG0ytJw3GZQiCIsI4kzGJcr4NiA'
            url = f'https://testsentry.pdc.org/hp_srv/services/hazard/{uuid}/exposure/latest/'
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
                                    'pdc': Pdc.objects.get(uuid=uuid)
                                }
                                PdcDisplacement.objects.get_or_create(**c_data)
