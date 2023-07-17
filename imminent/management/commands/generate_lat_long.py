import logging
import json

from django.core.management.base import BaseCommand
from shapely.geometry import Polygon
from shapely.geometry import mapping

from imminent.models import MeteoSwissAgg
from common.models import Country


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate Meteoswiss Lat/Lon"

    def get_latitude_longitude(self, geojson, country):
        if geojson and len(geojson) > 0:
            data = geojson["footprint_geojson"]["features"][0]
            if "geometry" in data and data["geometry"]:
                data = data["geometry"]["coordinates"]
                if len(data) == 1:
                    polygon_co = [tuple(x) for x in data[0]]
                    polygon = json.dumps(mapping(Polygon(polygon_co).centroid)["coordinates"])
                    pol = polygon.replace("[", "").replace("]", "")
                    polygon = pol.split(",")
                    return polygon[1], polygon[0]
                elif len(data) == 2:
                    polygon_co = [tuple(x) for x in data[0][0]]
                    polygon = json.dumps(mapping(Polygon(polygon_co).centroid)["coordinates"])
                    pol = polygon.replace("[", "").replace("]", "")
                    polygon = pol.split(",")
                    return polygon[1], polygon[0]
                else:
                    return None, None
            else:
                # get the coordinates from the country centroid
                country = Country.objects.get(id=country)
                centroid = country.centroid
                if "coordinates" in centroid:
                    lat = centroid["coordinates"][1]
                    lon = centroid["coordinates"][0]
                    return lat, lon
                else:
                    return None, None
        else:
            return None, None

    def handle(self, *args, **kwargs):
        for id, footprint_geojson, country in MeteoSwissAgg.objects.values_list("id", "geojson_details", "country"):
            # print(footprint_geojson)
            meteo = MeteoSwissAgg.objects.get(id=id)
            lat, lon = self.get_latitude_longitude(footprint_geojson, country)
            meteo.latitude = lat
            meteo.longitude = lon
            meteo.save()
