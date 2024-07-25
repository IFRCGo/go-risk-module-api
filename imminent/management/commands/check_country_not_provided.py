import logging
from functools import partial

import pyproj
from django.conf import settings
from django.core.management.base import BaseCommand
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.ops import transform

from common.models import Country
from imminent.models import Pdc, PdcDisplacement

logger = logging.getLogger(__name__)
proj_wgs84 = pyproj.Proj("+proj=longlat +datum=WGS84")


class Command(BaseCommand):
    """
    NOTE: Some of data sources don't provide country so check if they lies in
    country bbox
    """

    help = "Check latitude and longitude in bbox"

    def geodesic_point_buffer(self, lat, lon, km):
        # Azimuthal equidistant projection
        aeqd_proj = "+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0"
        project = partial(pyproj.transform, pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)), proj_wgs84)
        buf = Point(0, 0).buffer(km * 1000)  # distance in metres
        return transform(project, buf).exterior.coords[:]

    def handle(self, *args, **kwargs):
        """
        TODO: Add threshold for the country intersection?
        """
        # Get pdc whose country is null
        pdcdisplacment_queryset = PdcDisplacement.objects.filter(country__isnull=True, pdc__status=Pdc.Status.ACTIVE)
        countries_queryset = Country.objects.all()
        for displacement in pdcdisplacment_queryset:
            latitude = displacement.pdc.latitude
            longitude = displacement.pdc.longitude
            point = Point(latitude, longitude)
            for country in countries_queryset:
                if country.bbox:
                    [new_list] = country.bbox["coordinates"]
                    polygon_co = [tuple(x) for x in new_list]
                    polygon = Polygon(polygon_co)
                    if point.within(polygon):
                        displacement.country = country
                        displacement.save(update_fields=["country"])
                    else:
                        buffer_polygon = Polygon(
                            self.geodesic_point_buffer(latitude, longitude, settings.BUFFER_DISTANCE_IN_KM)
                        )  # passing buffer distance for now
                        if buffer_polygon.intersects(polygon):
                            displacement.country = country
                            displacement.save(update_fields=["country"])
