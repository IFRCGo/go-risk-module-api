import logging

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from django.core.management.base import BaseCommand

from common.models import Country
from imminent.models import Pdc, PdcDisplacement

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    NOTE: Some of data sources don't provide country so check if they lies in
    country bbox
    """
    help = 'Check latitude and longitude in bbox'

    def handle(self, *args, **kwargs):
        # Get pdc whose country is null
        pdcdisplacment_queryset = PdcDisplacement.objects.filter(
            country__isnull=True,
            pdc__status=Pdc.Status.ACTIVE
        )
        countries_queryset = Country.objects.all()
        for displacement in pdcdisplacment_queryset:
            latitude = displacement.pdc.latitude
            longitude = displacement.pdc.longitude
            point = Point(latitude, longitude)
            for country in countries_queryset:
                if country.bbox:
                    [new_list] = country.bbox['coordinates']
                    polygon_co = [tuple(x) for x in new_list]
                    polygon = Polygon(polygon_co)
                    if point.within(polygon):
                        displacement.country = country
                        displacement.save(update_fields=['country'])
