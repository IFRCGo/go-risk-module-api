import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from sentry_sdk.crons import monitor

from risk_module.sentry import SentryMonitor
from imminent.models import Pdc
from common.models import HazardType


class Command(BaseCommand):
    help = "Import polygon from `uuid` from pdc arch-gis"

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_INTENSITY)
    def handle(self, *args, **kwargs):
        # get all the uuids and use them to query to the
        # arch-gis server of pdc
        # filtering only cyclone since they only have track of disaster path
        uuids = Pdc.objects.filter(status=Pdc.Status.ACTIVE, hazard_type=HazardType.CYCLONE).values_list("uuid", flat=True)
        for uuid in uuids:
            session = requests.Session()
            login_url = "https://partners.pdc.org/arcgis/tokens/generateToken"

            data = {
                "f": "json",
                "username": settings.PDC_USERNAME,
                "password": settings.PDC_PASSWORD,
                "referer": "https://www.arcgis.com",
            }

            login_response = session.post(login_url, data=data, allow_redirects=True)
            access_token = login_response.json()["token"]
            session.headers.update(
                {
                    "Authorization": f"Bearer {access_token}",
                }
            )
            arch_gis_url = f"https://partners.pdc.org/arcgis/rest/services/partners/pdc_active_hazards_partners/MapServer/9/query?where=uuid%3D%27{uuid}%27&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=forecast_date_time%2Cwind_speed_mph%2Cseverity%2Cstorm_name%2Ctrack_heading&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&having=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson"  # noqa: E501
            arch_response = session.get(url=arch_gis_url)
            response_data = arch_response.json()
            update_data = []
            for data in response_data["features"]:
                update_data.append(data)
            for pdc in Pdc.objects.filter(uuid=uuid):
                pdc.storm_position_geojson = update_data
                pdc.save(update_fields=["storm_position_geojson"])
