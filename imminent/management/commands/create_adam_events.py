import logging
from datetime import datetime

import pytz
import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from common.models import Country, HazardType
from common.utils import logging_response_context
from imminent.models import Adam

logger = logging.getLogger(__name__)


def get_timezone_aware_datetime(iso_format_datetime) -> datetime:
    _datetime = datetime.fromisoformat(iso_format_datetime)
    if _datetime.tzinfo is None:
        _datetime = _datetime.replace(tzinfo=pytz.UTC)
    return _datetime


# TODO: Confirm if this is used or superseed by create_adam_exposure?
class Command(BaseCommand):
    help = "Import ADAM Event Data"

    def map_hazard_type(self, hazard_type):
        if hazard_type == "Earthquake":
            return HazardType.EARTHQUAKE
        elif hazard_type == "Flood":
            return HazardType.FLOOD
        elif hazard_type == "Tropical Storm":
            return HazardType.CYCLONE
        return

    def parse_datetime(self, date):
        return datetime.strptime(date, "%Y-%m-%dT%HH:MM::SS").strftime("%Y-%m-%d")

    def handle(self, **_):
        response = requests.get(f"{settings.WFP_ADAM}/events/feed")
        if response.status_code != 200:
            logger.error(
                "Error querying events feed data",
                extra=logging_response_context(response),
            )
            return
        values = response.json()

        for data in values:
            if data["eventType"] in ["Earthquake", "Flood", "Tropical Storm"]:
                adam = {
                    "title": data["title"],
                    "hazard_type": self.map_hazard_type(data["eventType"]),
                    "country": Country.objects.filter(iso3=data["eventISO3"].lower()).first(),
                    "event_id": data["guid"].split("_")[0] if data["eventType"] == "Tropical Storm" else data["guid"],
                    "publish_date": get_timezone_aware_datetime(data["pubDate"]),
                }
                Adam.objects.create(**adam)
