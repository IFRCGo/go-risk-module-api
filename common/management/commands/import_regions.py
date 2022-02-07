import requests

from django.core.management.base import BaseCommand

from common.models import Region


class Command(BaseCommand):
    help = 'Import Country'

    def handle(self, *args, **options):
        url = "https://dsgocdnapi.azureedge.net/api/v2/region/"
        response = requests.get(url)
        response_data = response.json()
        for data in response_data['results']:
            data = {
                'region_id': data['name'],
                'region_name': data['region_name'],
            }
            Region.objects.create(**data)
