import requests
import logging
import pandas as pd
import urllib
import numpy as np

from django.core.management.base import BaseCommand

from imminent.models import GDACS
from common.models import HazardType, Country


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    # NOTE: Source GDACS
    help = 'Import Active Hazards From Gdacs'

    def parse_hazard_type(self, hazard_type):
        hazard_dict = {
            'EQ': HazardType.EARTHQUAKE,
            'FL': HazardType.FLOOD,
            'TC': HazardType.CYCLONE,
            'DR': HazardType.DROUGHT,
            'WF': HazardType.WILDFIRE,
        }
        return hazard_dict.get(hazard_type)

    def handle(self, *args, **kwargs):
        # get the hazards occured in last
        url = 'https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH'
        response = requests.get(url)
        if response.status_code != 200:
            error_log = f'Error querying GDACS data at {url}'
            logger.error(error_log)
            logger.error(response.content)
        response_data = response.json()
        for old_data in response_data['features']:
            # basics data to be stored as
            episode_id = old_data['properties']['episodeid']
            event_id = old_data['properties']['eventid']
            location = old_data['bbox']
            if GDACS.objects.filter(hazard_id=event_id).exists():
                continue
            else:
                data = {
                    'hazard_id': old_data['properties']['eventid'],
                    'hazard_name': old_data['properties']['eventname'] if old_data['properties']['eventname'] != '' else old_data['properties']['htmldescription'],
                    'start_date': old_data['properties']['fromdate'],
                    'end_date': old_data['properties']['todate'],
                    'alert_level': old_data['properties']['alertlevel'],
                    'country': Country.objects.filter(iso3=old_data['properties']['iso3'].lower()).first(),
                    'event_details': old_data['properties'],
                    'hazard_type': self.parse_hazard_type(old_data['properties']['eventtype']),
                    'latitude': location[1],
                    'longitude': location[0]
                }
