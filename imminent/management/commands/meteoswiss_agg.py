import logging
import json

from django.core.management.base import BaseCommand
from django.db import models
from django.db.models import Max, Min
from shapely.geometry import Polygon, MultiPolygon
from shapely.geometry import mapping

from imminent.models import MeteoSwiss, MeteoSwissAgg
from common.models import HazardType, Country

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Aggregated Meteoswiss Data'

    def get_latitude_longitude(self, geojson):
        if geojson and len(geojson) > 0:
            data = geojson['footprint_geojson']['features'][0]['geometry']['coordinates']
            if len(data) == 1:
                polygon_co = [tuple(x) for x in data[0]]
                polygon = json.dumps(mapping(Polygon(polygon_co).centroid)['coordinates'])
                pol = polygon.replace('[', '').replace(']', '')
                polygon = pol.split(',')
                return polygon[1], polygon[0]
            elif len(data) == 2:
                polygon_co = [tuple(x) for x in data[0][0]]
                polygon = json.dumps(mapping(Polygon(polygon_co).centroid)['coordinates'])
                pol = polygon.replace('[', '').replace(']', '')
                polygon = pol.split(',')
                return polygon[1], polygon[0]
            else:
                return None, None
        else:
            return None, None

    def handle(self, *args, **kwargs):
        # get the meteoswiss data create an aggregated view for that
        events = MeteoSwiss.objects.values('hazard_name', 'country__name').distinct().annotate(
            start_date=Min('initialization_date'),
            end_date=Max('event_date'),
        )
        for event in list(events):
            new_dict = {}
            for data in MeteoSwiss.objects.filter(
                    impact_type='exposed_population_18mps',
                    footprint_geojson__isnull=False,
            ).order_by('initialization_date')[:1]:
                new_dict = {
                    'id': data.id,
                    'impact_type': data.impact_type,
                    'footprint_geojson': data.footprint_geojson,
                }
            event_details_dict = [
                {
                    'id': data.id,
                    'impact_type': data.impact_type,
                    'max': data.event_details.get('max'),
                    'mean': data.event_details.get('mean'),
                    'min': data.event_details.get('min'),
                } for data in MeteoSwiss.objects.filter(
                    hazard_name=event['hazard_name'],
                    country__name=event['country__name']
                ).order_by('initialization_date')
            ]
            details = {
                x['impact_type']: x for x in event_details_dict
            }.values()
            lat, lon = self.get_latitude_longitude(new_dict)
            data = {
                'country': Country.objects.filter(name__icontains=event['country__name']).first(),
                'hazard_name': event['hazard_name'],
                'start_date': event['start_date'],
                'event_details': list(details),
                'hazard_type': HazardType.CYCLONE,
                'end_date': event['end_date'],
                'geojson_details': new_dict,
                'latitude': lat,
                'longitude': lon,
            }
            MeteoSwissAgg.objects.create(**data)
