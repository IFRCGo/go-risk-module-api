import urllib3
import json
from datetime import datetime

from django.core.management.base import BaseCommand

from common.models import Country, HazardType
from imminent.models import Adam


class Command(BaseCommand):
    help = 'Import ADAM Exposure Data'

    def parse_datetime(self, date):
        return datetime.strptime(date, '%Y-%m-%dT%HH:MM::SS').strftime('%Y-%m-%d')

    def handle(self, *args, **kwargs):
        http = urllib3.PoolManager()

        earthquake_url = f'https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/earthquakes/'
        response = http.request('GET', earthquake_url)
        data = response.data
        eathquake_values = json.loads(data)
        for earthquake_event in eathquake_values['features']:
            data = {
                "geojson": earthquake_event['geometry'],
                "event_details": earthquake_event['properties'],
            }
            props = earthquake_event['properties']
            data.update(
                {
                    "country": Country.objects.filter(iso3=props['iso3'].lower()).first(),
                    "title": props['title'],
                    "hazard_type": HazardType.EARTHQUAKE,
                    "publish_date": props['published_at'],
                    "event_id": props['event_id'],
                })
            Adam.objects.create(**data)

        flood_url = f'https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/floods/'
        response = http.request('GET', flood_url)
        data = response.data
        flood_values = json.loads(data)
        for flood_event in flood_values['features']:
            data = {
                "geojson": flood_event['geometry'],
                "event_details": flood_event['properties'],
            }
            props = flood_event['properties']
            data.update(
                {
                    "country": Country.objects.filter(iso3=props['iso3'].lower()).first(),
                    "title": None,
                    "hazard_type": HazardType.FLOOD,
                    "publish_date": props['effective_date'],
                    "event_id": props['eventid'],
                })
            Adam.objects.create(**data)

        cyclone_url = f'https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/cyclones/'
        response = http.request('GET', cyclone_url)
        data = response.data
        cyclone_values = json.loads(data)
        for cyclone_event in cyclone_values['features']:
            data = {
                "geojson": cyclone_event['geometry'],
                "event_details": cyclone_event['properties'],
            }
            props = cyclone_event['properties']
            data.update(
                {
                    "country": Country.objects.filter(iso3=props['iso3'].lower()).first(),
                    "title": props['title'],
                    "hazard_type": HazardType.CYCLONE,
                    "publish_date": props['published_at'],
                    "event_id": props['event_id'],
                })
            Adam.objects.create(**data)
