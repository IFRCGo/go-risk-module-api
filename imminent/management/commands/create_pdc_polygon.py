import requests
import logging
import os

from django.core.management.base import BaseCommand

from imminent.models import Pdc


class Command(BaseCommand):
    help = "Import polygon from `uuid` from pdc arch-gis"

    def handle(self, *args, **kwargs):
        # get all the uuids and use them to query to the
        # arch-gis server of pdc
        uuids = Pdc.objects.filter(status=Pdc.Status.ACTIVE).values_list("uuid", flat=True)
        username = os.environ.get("PDC_USERNAME")
        password = os.environ.get("PDC_PASSWORD")
        for uuid in uuids:
            session = requests.Session()
            login_url = "https://partners.pdc.org/arcgis/tokens/generateToken"

            data = {
                "f": "json",
                "username": username,
                "password": password,
                "referer": "https://www.arcgis.com",
            }

            login_response = session.post(login_url, data=data, allow_redirects=True)
            access_token = login_response.json()["token"]

            session.headers.update(
                {
                    "Authorization": f"Bearer {access_token}",
                }
            )
            arch_gis_url = f"https://partners.pdc.org/arcgis/rest/services/partners/pdc_hazard_exposure/MapServer/27/query?where=hazard_uuid%3D%27{uuid}%27&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&having=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson"
            arch_response = session.get(url=arch_gis_url)
            response_data = arch_response.json()
            for data in response_data["features"]:
                features = data
                for pdc in Pdc.objects.filter(uuid=uuid):
                    pdc.footprint_geojson = features
                    pdc.save(update_fields=["footprint_geojson"])
