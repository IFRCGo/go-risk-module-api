import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

# from common.models import HazardType
from imminent.models import Pdc
from risk_module.sentry import SentryMonitor


class Command(BaseCommand):
    help = "Get PDC 3 days Cone of Uncertainty data"

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_THREE_DAYS_COU)
    def handle(self, *args, **kwargs):
        # get all the uuids and use them to query to the
        # arch-gis server of pdc
        # filtering only cyclone since they only have track of disaster path

        #uuids = Pdc.objects.filter(status=Pdc.Status.ACTIVE, hazard_type=HazardType.CYCLONE).values_list("uuid", flat=True)

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
        arch_gis_url = "https://partners.pdc.org/arcgis/rest/services/partners/pdc_active_hazards_partners/MapServer/12/query?where=uuid+is+not+null&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=hazard_name%2C+storm_name%2C+advisory_number%2C+severity%2C+objectid%2C+shape%2C+ESRI_OID%2C+category_id%2C+uuid%2C+hazard_id&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&having=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson"  # noqa: E501
        arch_response = session.get(url=arch_gis_url)
        response_data = arch_response.json()

        if response_data:
            update_data = {}
            for data in response_data["features"]:
                uuid = data["properties"]["uuid"]
                if uuid in update_data:
                    update_data[uuid]["features"].append(data)
                else:
                    update_data[uuid] = {
                        "type": "FeatureCollection",
                        "features": [data]
                    }

            for uuid, data in update_data.items():
                for pdc in Pdc.objects.filter(uuid=uuid):
                    pdc.cyclone_three_days_cou = data
                    pdc.save(update_fields=["cyclone_three_days_cou"])
