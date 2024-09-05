import typing

from django.core.management.base import BaseCommand
from django.db import models
from sentry_sdk.crons import monitor

from common.models import HazardType
from imminent.models import Pdc
from imminent.sources.pdc import ArcGisPdcSource
from risk_module.sentry import SentryMonitor


class Command(ArcGisPdcSource.CommandMixin, BaseCommand):
    help = "Get PDC 5 days Cone of Uncertainty data"

    def get_pdc_queryset(self) -> models.QuerySet[Pdc]:
        return super().get_pdc_queryset().filter(hazard_type=HazardType.CYCLONE)

    def save_pdc_using_uuid(self, session, uuid_list: typing.List[str]) -> bool:
        """
        Query and save pdc polygon data from Arc GIS for given uuids
        """
        # Fetch data for multiple uuids
        url = (
            "https://partners.pdc.org/arcgis/rest/services/partners/pdc_active_hazards_partners/MapServer/13/query"  # noqa: E501
        )
        response = session.post(
            url=url,
            data={
                **ArcGisPdcSource.ARC_GIS_DEFAULT_PARAMS,
                # NOTE: Each new request has 6s+ response time, using where in query we reduce that latency
                "where": self.generate_uuid_where_statement("uuid", uuid_list),
                "outFields": (
                    "uuid,"
                    "hazard_name,storm_name,advisory_number,severity,objectid,shape,ESRI_OID,category_id,source,uuid,hazard_id"
                ),
            },
        )

        # Save data for multiple uuids
        response_data = response.json()

        is_valid = self.is_valid_arc_response(response_data)
        if not is_valid:
            return False

        for feature in response_data["features"]:
            # XXX: Multiple row has same uuid
            _uuid = feature["properties"].pop("uuid")
            Pdc.objects.filter(uuid=_uuid).update(
                cyclone_five_days_cou=feature,
            )
        return True

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_FIVE_DAYS_COU)
    def handle(self, **_):
        self.process()
