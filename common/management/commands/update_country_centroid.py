import requests

from django.core.management.base import BaseCommand

from common.models import Country


class Command(BaseCommand):
    help = "Update Country bbox"

    def handle(self, *args, **options):
        url = "https://goadmin-stage.ifrc.org/api/v2/country/"
        while url:
            response = requests.get(url)
            response_data = response.json()
            url = response_data['next']
            for data in response_data['results']:
                centroid = data['centroid']
                iso3 = data['iso3']
                if iso3:
                    country = Country.objects.filter(iso3=iso3.lower())
                    if country.exists():
                        country = country.first()
                        country.centroid = centroid
                        country.save(update_fields=['centroid'])
