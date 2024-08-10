import json
import logging
import typing
from datetime import datetime

import pytz
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from common.models import Country, HazardType
from common.utils import logging_response_context
from imminent.models import Adam
from risk_module.sentry import SentryMonitor

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
    def process_response(response: requests.Response) -> typing.Optional[dict]:
        if response.status_code != 200:
            return None

        try:
            data = response.json()
        except json.JSONDecodeError:
            return None

        if isinstance(data, dict) and "features" not in data:
            return None
        return data

    def process_earthquakes(self, http_session: requests.Session):
        response = http_session.get(f"{settings.WFP_ADAM}/events/earthquakes/")
        response_data = self.process_response(response)

        if response_data is None:
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

    def process_floods(self, http_session: requests.Session):
        response = http_session.get(f"{settings.WFP_ADAM}/events/floods/")
        response_data = self.process_response(response)

        if response_data is None:
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

    def process_cyclones(self, http_session: requests.Session):
        response = http_session.get(f"{settings.WFP_ADAM}/events/cyclones/")
        response_data = self.process_response(response)

        if response_data is None:
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
            for country in countries_props:  # XXX: Why not just select the last countries_props?
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
    def handle(self, **_):
        http_session = requests.Session()
        self.process_earthquakes(http_session)
        self.process_floods(http_session)
        self.process_cyclones(http_session)
