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
                independent = data['independent']
                is_deprecated = data['is_deprecated']
                record_type = data['record_type']
                print(record_type)
                iso3 = data['iso3']
                if iso3:
                    country = Country.objects.filter(iso3=iso3.lower())
                    if country.exists():
                        country = country.last()
                        country.independent = independent
                        country.is_deprecated = is_deprecated
                        country.record_type = record_type
                        country.save(update_fields=['independent', 'is_deprecated', 'record_type'])
            cluster_country_name = [
                'West Africa Country Cluster',
                'Tunis Country Cluster',
                'Suva Country Cluster',
                'Southern Cone Country Cluster',
                'Southern Africa Country Cluster',
                'South Caucasus Country Cluster',
                'South America Country Cluster',
                'North America and Mexico Country Cluster',
                'New Delhi Country Cluster',
                'Moscow Country Cluster',
                'Jakarta Country Cluster',
                'Indian Ocean Islands Country Cluster',
                'East Africa Country Cluster',
                'Dubai Country Cluster',
                'Cuba, Haiti and Dominican Republic Country Cluster',
                'Central and South-Eastern Europe Country Cluster',
                'Central Asia Country Cluster',
                'Central America Country Cluster',
                'Central Africa Country Cluster',
                'Caribbean Country Cluster',
                'Beijing Country Cluster',
                'Bangkok Country Cluster',
            ]
            for name in cluster_country_name:
                Country.objects.filter(name=name).update(record_type=Country.CountryType.CLUSTER)
