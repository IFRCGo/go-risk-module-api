import datetime

import requests
from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from common.models import HazardType
from imminent.models import Pdc
from risk_module.sentry import SentryMonitor

from .create_pdc_polygon import ARC_GIS_DEFAULT_PARAMS
from .create_pdc_polygon import Command as CreatePdcPolygonCommand


class Command(BaseCommand):
    help = "Import polygon from `uuid` from pdc arc-gis"

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_INTENSITY)
    def handle(self, **_):
        # get all the uuids and use them to query to the
        # arc-gis server of pdc
        # filtering only cyclone since they only have track of disaster path
        uuids = Pdc.objects.filter(status=Pdc.Status.ACTIVE, hazard_type=HazardType.CYCLONE).values_list("uuid", flat=True)
        session = requests.Session()
        token_expires = None

        for uuid in uuids:
            # Attach auth token
            if token_expires is None or datetime.datetime.now() >= token_expires:
                access_token, token_expires = CreatePdcPolygonCommand.get_access_token(session)
                session.headers.update(
                    {
                        "Authorization": f"Bearer {access_token}",
                    }
                )

            # Fetch
            arc_gis_url = "https://partners.pdc.org/arcgis/rest/services/partners/pdc_active_hazards_partners/MapServer/9/query"
            arc_response = session.post(
                url=arc_gis_url,
                data={
                    **ARC_GIS_DEFAULT_PARAMS,
                    "where": f"uuid='{uuid}'",
                    "outFields": "forecast_date_time,wind_speed_mph,severity,storm_name,track_heading",
                },
            )

            # Save to database
            response_data = arc_response.json()
            Pdc.objects.filter(uuid=uuid).update(
                storm_position_geojson=response_data["features"],
            )
