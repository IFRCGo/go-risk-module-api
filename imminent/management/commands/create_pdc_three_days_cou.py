import datetime

import requests
from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from common.models import HazardType
from imminent.models import Pdc
from risk_module.sentry import SentryMonitor

from .create_pdc_polygon import ARC_GIS_DEFAULT_PARAMS
from .create_pdc_polygon import Command as CreatePdcDataCommand


class Command(BaseCommand):
    help = "Get PDC 3 days Cone of Uncertainty data"

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_THREE_DAYS_COU)
    def handle(self, *args, **kwargs):
        # get all the uuids and use them to query to the
        # arc-gis server of pdc
        # filtering only cyclone since they only have track of disaster path

        uuids = Pdc.objects.filter(status=Pdc.Status.ACTIVE, hazard_type=HazardType.CYCLONE).values_list("uuid", flat=True)

        session = requests.Session()
        token_expires = None

        arc_gis_url = (
            "https://partners.pdc.org/arcgis/rest/services/partners/pdc_active_hazards_partners/MapServer/12/query"  # noqa: E501
        )

        for uuid in uuids:
            if token_expires is None or datetime.datetime.now() >= token_expires:
                access_token, token_expires = CreatePdcDataCommand.get_access_token(session)
                session.headers.update({"Authorization": f"Bearer {access_token}"})

            # Fetch
            arc_response = session.post(
                url=arc_gis_url,
                data={
                    **ARC_GIS_DEFAULT_PARAMS,
                    "where": f"uuid='{uuid}'",
                    "outFields": "hazard_name,storm_name,advisory_number,objectid,ESRI_OID,category_id,uuid",  # noqa: E501
                },
            )

            if arc_response.status_code == 200:
                response_data = arc_response.json()
                Pdc.objects.filter(uuid=uuid).update(cyclone_three_days_cou=response_data)
