import requests
import logging

from django.core.management.base import BaseCommand

from ipc.models import (
    HazardType,
    ThinkHazardCountry,
    ThinkHazardInformation,
    Country
)

logger = logging.getLogger()


class Command(BaseCommand):
    help = 'Create ThinkHazardInformation'


    def parse_hazard_level(self, hazard_level):
        if hazard_level == 'Low':
            hazard_level = ThinkHazardInformation.ThinkHazardLevel.LOW
        elif hazard_level == 'Very low':
            hazard_level = ThinkHazardInformation.ThinkHazardLevel.VERY_LOW
        elif hazard_level == 'Medium':
            hazard_level = ThinkHazardInformation.ThinkHazardLevel.MEDIUM
        elif hazard_level == 'High':
            hazard_level = ThinkHazardInformation.ThinkHazardLevel.HIGH
        return hazard_level

    def handle(self, **options):
        # listing the hazard type to be mapped from the thinkhazard
        HazadTypeList = [HazardType.CYCLONE, HazardType.DROUGHT, HazardType.FLOOD]
        hazardTypeThinkHazard = ['CY', 'FL', 'DR']
        # list down the country from thinkhazard_country
        countries = ThinkHazardCountry.objects.all().values_list('iso3', 'country_id')
        for iso3, country_id in countries:
            for hazard_type in hazardTypeThinkHazard:
                if hazard_type == 'CY':
                    map_hazard_type = HazadTypeList[0]
                elif hazard_type == 'FL':
                    map_hazard_type = HazadTypeList[1]
                elif hazard_type == 'DR':
                    map_hazard_type = HazadTypeList[2]
                url = f'https://thinkhazard.org/en/report/{country_id}/{hazard_type}.json'
                response = requests.get(url)
                if response.status_code == 200:
                    hazard_data = response.json()
                    if Country.objects.filter(iso3=iso3.lower()).exists():
                        data = {
                            'country': Country.objects.filter(iso3=iso3.lower()).first(),
                            'hazard_type': map_hazard_type,
                            'hazard_level': self.parse_hazard_level(hazard_data['hazard_category']['hazard_level']),
                            'information': hazard_data['hazard_category']['general_recommendation']
                        }
                        ThinkHazardInformation.objects.create(**data)
