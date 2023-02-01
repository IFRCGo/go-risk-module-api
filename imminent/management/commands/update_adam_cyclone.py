import urllib3
import json
from datetime import datetime

from django.core.management.base import BaseCommand

from common.models import Country, HazardType
from imminent.models import Adam


class Command(BaseCommand):
    help = 'Import ADAM Cyclone Geojson'

    def handle(self, *args, **kwargs):
        http = urllib3.PoolManager()
        cyclone_event_id = Adam.objects.filter(
            hazard_type=HazardType.CYCLONE
        )
        for event in cyclone_event_id:
            cyclone_url = f'https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/cyclones/{event.event_id}'
            response = http.request('GET', cyclone_url)
            data = response.data
            cyclone_data = json.loads(data)
            event.storm_position_geojson = cyclone_data
            event.save(update_fields=['storm_position_geojson'])

