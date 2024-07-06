import urllib3
import json
import pytz
from datetime import datetime

from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from risk_module.sentry import SentryMonitor
from common.models import Country, HazardType
from imminent.models import Adam


def get_timezone_aware_datetime(iso_format_datetime) -> datetime:
    _datetime = datetime.fromisoformat(iso_format_datetime)
    if _datetime.tzinfo is None:
        _datetime = _datetime.replace(tzinfo=pytz.UTC)
    return _datetime


class Command(BaseCommand):
    help = "Import ADAM Exposure Data"

    def parse_datetime(self, date):
        return datetime.strptime(date, "%Y-%m-%dT%HH:MM::SS").strftime("%Y-%m-%d")

    @monitor(monitor_slug=SentryMonitor.CREATE_ADAM_EXPOSURE)
    def handle(self, *args, **kwargs):
        http = urllib3.PoolManager()

        earthquake_url = "https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/earthquakes/"
        response = http.request("GET", earthquake_url)
        data = response.data
        eathquake_values = json.loads(data)
        for earthquake_event in eathquake_values["features"]:
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

        flood_url = "https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/floods/"
        response = http.request("GET", flood_url)
        data = response.data
        flood_values = json.loads(data)
        for flood_event in flood_values["features"]:
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

        cyclone_url = "https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/cyclones/"
        response = http.request("GET", cyclone_url)
        data = response.data
        cyclone_values = json.loads(data)
        for cyclone_event in cyclone_values["features"]:
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
