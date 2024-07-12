import logging
import urllib3
import json
import pytz
from datetime import datetime

from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from risk_module.sentry import SentryMonitor
from common.models import Country, HazardType
from common.utils import logging_response_context
from imminent.models import Adam


logger = logging.getLogger(__name__)


def get_timezone_aware_datetime(iso_format_datetime) -> datetime:
    _datetime = datetime.fromisoformat(iso_format_datetime)
    if _datetime.tzinfo is None:
        _datetime = _datetime.replace(tzinfo=pytz.UTC)
    return _datetime


class Command(BaseCommand):
    help = "Import ADAM Exposure Data"

    def parse_datetime(self, date):
        return datetime.strptime(date, "%Y-%m-%dT%HH:MM::SS").strftime("%Y-%m-%d")

    @staticmethod
    def is_response_valid(response, response_data) -> bool:
        if (
            response.status != 200 or
            (
                isinstance(response_data, dict) and
                "features" not in response_data
            )
        ):
            return False
        return True

    def process_earthquakes(self, http):
        earthquake_url = "https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/earthquakes/"
        response = http.request("GET", earthquake_url)
        response_data = json.loads(response.data)

        if not self.is_response_valid(response, response_data):
            logger.error(
                "Error querying Adam Earthquakes data",
                extra=logging_response_context(response),
            )
            return

        for earthquake_event in response_data["features"]:
            geojson = {
                "type": "Feature",
                "geometry": earthquake_event["geometry"],
                "properties": {},
            }
            mag = earthquake_event["properties"].get("mag")
            if mag:
                if mag < 6.2:
                    earthquake_event["properties"]["alert_level"] = "Green"
                elif mag > 6 and mag <= 6.5:
                    earthquake_event["properties"]["alert_level"] = "Orange"
                elif mag > 6.5:
                    earthquake_event["properties"]["alert_level"] = "Red"
            data = {
                "geojson": geojson,
                "event_details": earthquake_event["properties"],
            }
            props = earthquake_event["properties"]
            data.update(
                {
                    "country": Country.objects.filter(iso3=props["iso3"].lower()).last(),
                    "title": props["title"],
                    "hazard_type": HazardType.EARTHQUAKE,
                    "publish_date": get_timezone_aware_datetime(props["published_at"]),
                    "event_id": props["event_id"],
                }
            )
            Adam.objects.get_or_create(**data)

    def process_floods(self, http):
        flood_url = "https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/floods/"
        response = http.request("GET", flood_url)
        response_data = json.loads(response.data)

        if not self.is_response_valid(response, response_data):
            logger.error(
                "Error querying Adam Floods data",
                extra=logging_response_context(response),
            )
            return

        for flood_event in response_data["features"]:
            geojson = {
                "type": "Feature",
                "geometry": flood_event["geometry"],
                "properties": {},
            }
            data = {
                "geojson": geojson,
                "event_details": flood_event["properties"],
            }
            props = flood_event["properties"]
            data.update(
                {
                    "country": Country.objects.filter(iso3=props["iso3"].lower()).last(),
                    "title": None,
                    "hazard_type": HazardType.FLOOD,
                    "publish_date": get_timezone_aware_datetime(props["effective_date"]),
                    "event_id": props["eventid"],
                }
            )
            Adam.objects.get_or_create(**data)

    def process_cyclones(self, http):
        cyclone_url = "https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/cyclones/"
        response = http.request("GET", cyclone_url)
        response_data = json.loads(response.data)

        if not self.is_response_valid(response, response_data):
            logger.error(
                "Error querying Adam Cyclones data",
                extra=logging_response_context(response),
            )
            return

        for cyclone_event in response_data["features"]:
            data = {
                "geojson": cyclone_event["geometry"],
                "event_details": cyclone_event["properties"],
            }
            props = cyclone_event["properties"]
            # check for countries here
            # using only iso3 here isn't suitable for extracting the population exposure
            countries_props = cyclone_event["properties"]["countries"].split(",")
            for country in countries_props:
                data.update(
                    {
                        "country": Country.objects.filter(name__icontains=country.strip()).last(),
                        "title": props["title"],
                        "hazard_type": HazardType.CYCLONE,
                        "publish_date": get_timezone_aware_datetime(props["published_at"]),
                        "event_id": props["event_id"],
                    }
                )
                Adam.objects.get_or_create(**data)

    @monitor(monitor_slug=SentryMonitor.CREATE_ADAM_EXPOSURE)
    def handle(self, *args, **kwargs):
        http = urllib3.PoolManager()
        self.process_earthquakes(http)
        self.process_floods(http)
        self.process_cyclones(http)
