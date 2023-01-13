import logging
import urllib3
import json
from datetime import datetime

from django.core.management.base import BaseCommand

from common.models import Country, HazardType
from imminent.models import Adam


logger = logging.getLogger()


class Command(BaseCommand):
    help = 'Import ADAM Event Data'

    def map_hazard_type(self, hazard_type):
        if hazard_type == 'Earthquake':
            return HazardType.EARTHQUAKE
        elif hazard_type == 'Flood':
            return HazardType.FLOOD
        elif hazard_type == 'Tropical Storm':
            return HazardType.CYCLONE
        return

    def parse_datetime(self, date):
        return datetime.strptime(date, '%Y-%m-%dT%HH:MM::SS').strftime('%Y-%m-%d')

    def handle(self, *args, **options):
        http = urllib3.PoolManager()
        url = 'https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/feed'
        response = http.request('GET', url)
        data = response.data
        values = json.loads(data)
        for data in values:
            if data['eventType'] in ['Earthquake', 'Flood', 'Tropical Storm']:
                adam = {
                    'title': data['title'],
                    'hazard_type': self.map_hazard_type(data['eventType']),
                    'country': Country.objects.filter(iso3=data['eventISO3'].lower()).first(),
                    'event_id': data['guid'].split('_')[0] if data['eventType'] == 'Tropical Storm' else data['guid'],
                    'publish_date': data['pubDate']
                }
                Adam.objects.create(**adam)
