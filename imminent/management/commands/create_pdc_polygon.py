import logging
import typing

from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from imminent.models import Pdc
from imminent.sources.pdc import ArcGisPdcSource
from risk_module.sentry import SentryMonitor

logger = logging.getLogger(__name__)


class Command(ArcGisPdcSource.CommandMixin, BaseCommand):
    help = "Import polygon from `uuid` from pdc arch-gis"

    def save_pdc_using_uuid(self, session, uuid_list: typing.List[str]) -> bool:
        """
        Query and save pdc polygon data from Arc GIS for given uuids
        """
        # Fetch data for multiple uuids
        url = "https://partners.pdc.org/arcgis/rest/services/partners/pdc_hazard_exposure/MapServer/27/query"
        response = session.post(
            url=url,
            data={
                **ArcGisPdcSource.ARC_GIS_DEFAULT_PARAMS,
                # NOTE: Each new request has 6s+ response time, using where in query we reduce that latency
                "where": self.generate_uuid_where_statement("hazard_uuid", uuid_list),
                "outFields": "hazard_uuid,type_id",
            },
        )

        # Save data for multiple uuids
        response_data = response.json()

        is_valid = self.is_valid_arc_response(response_data)
        if not is_valid:
            return False

        for feature in response_data["features"]:
            # XXX: Multiple row has same uuid
            _uuid = feature["properties"].pop("hazard_uuid")
            Pdc.objects.filter(uuid=_uuid).update(
                footprint_geojson=feature,
            )
        return True

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_POLYGON)
    def handle(self, **_):
        self.process()
