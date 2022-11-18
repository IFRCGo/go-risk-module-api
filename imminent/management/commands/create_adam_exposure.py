import urllib3
import json

from django.core.management.base import BaseCommand

from common.models import Country, HazardType
from imminent.models import Adam


class Command(BaseCommand):
    help = 'Import ADAM Exposure Data'

    def handle(self, *args, **kwargs):
        http = urllib3.PoolManager()

        # Filter Out events with hazard_type=`Earthquake`
        earthquake_events = Adam.objects.filter(
            hazard_type=HazardType.EARTHQUAKE
        )
        for event in earthquake_events:
            url = f'https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/earthquakes/{event.event_id}'
            response = http.request('GET', url)
            data = response.data
            values = json.loads(data)
            data = {
                "geometry": values['geometry'],
                "properties": values['properties'],
            }
            Adam.objects.filter(event_id=event.event_id).update(geojson=data)
            # adam.geojson = data
            # adam.save(update_fields=['geojson'])
        cyclone_events = Adam.objects.filter(
            hazard_type=HazardType.CYCLONE
        )
        for event in cyclone_events:
            url = f'https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/cyclones/{event.event_id}'
            response = http.request('GET', url)
            data = response.data
            values = json.loads(data)
            Adam.objects.filter(event_id=event.event_id).update(geojson=values)
            # adam.geojson = values
            # adam.save(update_fields=['geojson'])
