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
        if geojson:
            data = geojson['geojson'][0]['footprint_geojson']['features'][0]['geometry']['coordinates']
            if len(data) > 0:
                # polygon_co = [tuple(x) for x in data]
                new_data = [tuple(x) for x in data[0][0]]
                polygon = json.dumps(mapping(Polygon(new_data).centroid)['coordinates'])
                pol = polygon.replace('[', '').replace(']', '')
                polygon = pol.split(',')
                return polygon[1], polygon[0]

    def handle(self, *args, **kwargs):
        # get the meteoswiss data create an aggregated view for that
        events = MeteoSwiss.objects.values('hazard_name', 'country__name').distinct().annotate(
            start_date=Min('initialization_date'),
            end_date=Max('event_date'),
            event_details_dict=models.Value({
                'impacts': [
                    {
                        'id': data.id,
                        'imapct_type': data.impact_type,
                        'max': data.event_details.get('max'),
                        'mean': data.event_details.get('mean'),
                        'min': data.event_details.get('min'),
                    } for data in MeteoSwiss.objects.filter(
                        hazard_name=models.F('hazard_name'),
                        country=models.F('country')
                    )
                ]
            }, output_field=models.JSONField()),
            geojson_details_dict=models.Value({
                'geojson': [
                    {
                        'id': data.id,
                        'impact_type': data.impact_type,
                        'footprint_geojson': data.footprint_geojson,
                    } for data in MeteoSwiss.objects.filter(
                        hazard_name=models.F('hazard_name'),
                        country=models.F('country'),
                        impact_type='exposed_population_18mps',
                        initialization_date=models.F('initialization_date'),
                    )[:1]
                ]
            }, output_field=models.JSONField())
        )
        for event in list(events):
            lat, lon = self.get_latitude_longitude(event['geojson_details_dict'])
            data = {
                'country': Country.objects.filter(name__icontains=event['country__name']).first(),
                'hazard_name': event['hazard_name'],
                'start_date': event['start_date'],
                'event_details': event['event_details_dict'],
                'hazard_type': HazardType.CYCLONE,
                'end_date': event['end_date'],
                'geojson_details': event['geojson_details_dict'],
                'latitude': lat,
                'longitude': lon,
            }
            MeteoSwissAgg.objects.create(**data)
