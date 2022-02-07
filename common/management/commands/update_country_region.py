import requests

from django.core.management.base import BaseCommand

from common.models import Country, Region


class Command(BaseCommand):
    help = 'Import Country'

    def handle(self, *args, **options):
        url = "https://dsgocdnapi.azureedge.net/api/v2/country/"
        while url:
            response = requests.get(url)
            response_data = response.json()
            url = response_data['next']
            for data in response_data['results']:
                print(data)
                region = data['region']
                iso3 = data['iso3']
                if iso3:
                    if Country.objects.filter(iso3=iso3.lower()).exists():
                        country = Country.objects.filter(iso3=iso3.lower()).first()
                        region = Region.objects.filter(region_id=region)
                        if region.exists():
                            region = region.first()
                        else:
                            region = None
                        country.region = region
                        country.save(update_fields=['region'])
