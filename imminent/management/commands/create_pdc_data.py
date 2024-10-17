import datetime
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

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_DATA)
    def handle(self, **_):
        # Look for last updates for last X hours only
        # NOTE: If we don't use GREATER_THAN filter, then PDC will take a lot of time to respond with the data.
        # Ranging from few minutes to hours
        now = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=48)
        today_timestmap = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {
            "pagination": {"page": 1, "pagesize": 100},
            "order": {"orderlist": {"updateDate": "DESC"}},
            "restrictions": [[{"searchType": "GREATER_THAN", "updateDate": today_timestmap}]],
        }

        response = requests.post(
            SentryPdcSource.URL.PDC_SEARCH_HAZARD,
            headers=SentryPdcSource.authorization_headers(),
            json=data,
            timeout=10 * 60,
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
