import datetime
import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from sentry_sdk.crons import monitor

from common.models import HazardType
from common.utils import logging_response_context
from imminent.models import Pdc
from risk_module.sentry import SentryMonitor

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import Active Hazards"

    SEVERITY_MAP = {
        "WARNING": Pdc.Severity.WARNING,
        "WATCH": Pdc.Severity.WATCH,
        "ADVISORY": Pdc.Severity.ADVISORY,
        "INFORMATION": Pdc.Severity.INFORMATION,
    }

    HAZARD_TYPE_MAP = {
        "FLOOD": HazardType.FLOOD,
        "CYCLONE": HazardType.CYCLONE,
        "STORM": HazardType.STORM,
        "DROUGHT": HazardType.DROUGHT,
        "WIND": HazardType.WIND,
        "TSUNAMI": HazardType.TSUNAMI,
        "EARTHQUAKE": HazardType.EARTHQUAKE,
        "WILDFIRE": HazardType.WILDFIRE,
    }

    @staticmethod
    def parse_timestamp(timestamp):
        # NOTE: all timestamp are in millisecond and with timezone `utc`
        return timezone.make_aware(
            # FIXME: Using deprecated function
            datetime.datetime.utcfromtimestamp(int(timestamp) / 1000)
        )

    def save_pdc_data(self, hazard_type: HazardType, data):
        pdc_updated_at = self.parse_timestamp(data["last_Update"])

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
            "start_date": self.parse_timestamp(data["start_Date"]),
            "end_date": self.parse_timestamp(data["end_Date"]),
            "status": Pdc.Status.ACTIVE,
            "pdc_created_at": self.parse_timestamp(data["create_Date"]),
            "pdc_updated_at": pdc_updated_at,
            "severity": self.SEVERITY_MAP.get(data["severity_ID"].upper()),
        }
        Pdc.objects.get_or_create(**pdc_data)

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_DATA)
    def handle(self, **_):
        # NOTE: Use the search hazard api for the information download
        # make sure to use filter the data
        url = "https://sentry.pdc.org/hp_srv/services/hazards/t/json/search_hazard"
        headers = {"Authorization": "Bearer {}".format(settings.PDC_ACCESS_TOKEN)}
        # make sure to use the datetime now and timestamp for the post data
        # current date and time
        now = datetime.datetime.now()
        today_timestmap = str(datetime.datetime.timestamp(now)).replace(".", "")
        data = {
            "pagination": {"page": 1, "pagesize": 100},
            "order": {"orderlist": {"updateDate": "DESC"}},
            "restrictions": [[{"searchType": "LESS_THAN", "updateDate": today_timestmap}]],
        }
        response = requests.post(url, headers=headers, json=data)
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
                if hazard_type := self.HAZARD_TYPE_MAP.get(data["type_ID"].upper()):
                    self.save_pdc_data(hazard_type, data)
