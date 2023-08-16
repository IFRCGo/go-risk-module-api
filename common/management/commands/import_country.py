import requests

from django.core.management.base import BaseCommand

from common.models import Country


class Command(BaseCommand):
    help = 'Import Country'

    def handle(self, *args, **options):
        url = "https://goadmin-stage.ifrc.org/api/v2/country/"
        while url:
            response = requests.get(url)
            response_data = response.json()
            url = response_data['next']
            for data in response_data['results']:
                data = {
                    'name': data['name'],
                    'iso3': data['iso3'],
                    'iso': data['iso']
                }
                Country.objects.get_or_create(**data)
