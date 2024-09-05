import logging

import requests
from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from common.utils import logging_response_context
from imminent.models import Pdc
from imminent.sources.pdc import SentryPdcSource
from risk_module.sentry import SentryMonitor

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import Active Hazards"

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_DAILY)
    def handle(self, **_):
        response = requests.get(
            SentryPdcSource.URL.PDC_ACTIVE_HAZARD,
            headers=SentryPdcSource.authorization_headers(),
        )
        if response.status_code != 200:
            logger.error(
                "Error querying PDC data",
                extra=logging_response_context(response),
            )
            return

        response_data = response.json()
        for data in response_data:
            hazard_status = data["status"].upper()

            uuid = data["uuid"]
            # Tag expired hazards
            if hazard_status == "E":
                Pdc.objects.filter(uuid=uuid).update(status=Pdc.Status.EXPIRED)

            # Process active hazards
            elif hazard_status == "A":
                SentryPdcSource.save_pdc_data(uuid, SentryPdcSource.parse_response_data(data))
