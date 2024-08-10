import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from common.models import HazardType
from common.utils import logging_response_context
from imminent.models import Pdc
from risk_module.sentry import SentryMonitor

from .create_pdc_data import Command as CreatePdcDataCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import Active Hazards"

    def save_pdc_data(self, hazard_type: HazardType, data):
        pdc_updated_at = CreatePdcDataCommand.parse_timestamp(data["last_Update"])

        # XXX: This was only done for WILDFIRE before??
        existing_qs = Pdc.objects.filter(
            uuid=data["uuid"],
            hazard_type=hazard_type,
            pdc_updated_at=pdc_updated_at,
        )
        if existing_qs.exists():
            return

        pdc_data = {
            "hazard_id": data["hazard_ID"],
            "hazard_name": data["hazard_Name"],
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "description": data["description"],
            "hazard_type": hazard_type,
            "uuid": data["uuid"],
            "start_date": CreatePdcDataCommand.parse_timestamp(data["start_Date"]),
            "end_date": CreatePdcDataCommand.parse_timestamp(data["end_Date"]),
            "status": Pdc.Status.ACTIVE,
            "pdc_created_at": CreatePdcDataCommand.parse_timestamp(data["create_Date"]),
            "pdc_updated_at": pdc_updated_at,
            # XXX: Severity was not saved here compare to create_pdc_data
        }
        Pdc.objects.get_or_create(**pdc_data)

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_DAILY)
    def handle(self, **_):
        # NOTE: Use the search hazard api for the information download
        # make sure to use filter the data
        url = "https://sentry.pdc.org/hp_srv/services/hazards/t/json/get_active_hazards"
        headers = {"Authorization": "Bearer {}".format(settings.PDC_ACCESS_TOKEN)}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logger.error(
                "Error querying PDC data",
                extra=logging_response_context(response),
            )
            return

        response_data = response.json()
        for data in response_data:
            # NOTE: Filter the active hazard only
            # Update the hazard if it has expired
            hazard_status = data["status"]

            if hazard_status == "E":
                Pdc.objects.filter(uuid=data["uuid"]).update(status=Pdc.Status.EXPIRED)

            elif hazard_status == "A":
                if hazard_type := CreatePdcDataCommand.HAZARD_TYPE_MAP.get(data["type_ID"].upper()):
                    self.save_pdc_data(hazard_type, data)
