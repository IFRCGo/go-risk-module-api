import logging
import datetime

from django.core.management.base import BaseCommand

from imminent.models import Adam
from common.models import HazardType

logger = logging.getLogger()


class Command(BaseCommand):
    help = 'Update Adam GeoJson'

    def handle(self, *args, **options):
        adams = Adam.objects.filter(
            hazard_type__in=[HazardType.FLOOD, HazardType.EARTHQUAKE],
        )
        for adam in adams:
            adam_geojson = adam.geojson
            update_geojson = {
                "type": "Feature",
                "geometry": adam_geojson,
                "properties": {},
            }
            adam.geojson = update_geojson
            adam.save(update_fields=['geojson'])
