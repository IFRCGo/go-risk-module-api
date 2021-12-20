import requests

from django.core.management.base import BaseCommand

from ipc.models import Country


class Command(BaseCommand):
    help = 'Import Country'

    def handle(self, *args, **options):
        url = "https://go-api.togglecorp.com/api/v2/country/"
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
                Country.objects.create(**data)
