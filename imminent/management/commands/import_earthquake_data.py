import csv
import datetime
import logging
from functools import lru_cache

import requests
from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from sentry_sdk.crons import monitor

from common.models import Country
from common.utils import logging_response_context
from imminent.models import Earthquake
from risk_module.sentry import SentryMonitor

logger = logging.getLogger(__name__)


# XXX: Not used right now
class Command(BaseCommand):
    help = "Import Earthquake geo-locations from external api"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        geolocator = Nominatim(user_agent="risk_module_earthquake")
        self.reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

    def parse_timestamp(self, timestamp):
        # NOTE: all timestamp are in millisecond and with timezone `utc`
        return timezone.make_aware(datetime.datetime.utcfromtimestamp(timestamp / 1000))

    @lru_cache(maxsize=1000)  # Simple cache. TODO: Look for better way
    def get_country(self, latitude, longitude):
        location = self.reverse((latitude, longitude), language="en", exactly_one=True)
        if location and location.raw["address"].get("country"):
            return location.raw["address"]["country"]

    @monitor(monitor_slug=SentryMonitor.IMPORT_EARTHQUAKE_DATA)
    def handle(self, *args, **options):
        """
        NOTE: We will delete all the previous earthquake
              Call this api every day and try to pull data one week prior to today
        """
        # Delete all the previous earthquake
        Earthquake.objects.all().delete()
        # call the api to import data prior to one week from today
        now = timezone.now()
        today = now.date()
        seven_days_before = (now + relativedelta(days=-7)).date()
        logger.info("Starting data import")
        # NOTE: This is for the local test purpose only
        url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={seven_days_before}&endtime={today}"
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(
                "Error querying earthquake data",
                extra=logging_response_context(response),
            )
            # TODO: return?

        earthquake_data = response.json()
        header = [
            "event_id",
            "event_title",
            "event_place",
            "event_date",
            "updated_at",
            "latitude",
            "longitude",
            "depth",
            "magnitude",
            "magnitude_type",
            "country",
        ]
        all_data = []
        for earthquake in earthquake_data["features"]:
            event_id = earthquake["id"]
            magnitude = earthquake["properties"]["mag"]
            magnitude_type = earthquake["properties"]["magType"]

            if magnitude is None or magnitude_type is None:
                logger.warning(f"Skipping data for event_id: {event_id}. {magnitude=} or {magnitude_type} is None")
                continue

            country_name = self.get_country(earthquake["geometry"]["coordinates"][1], earthquake["geometry"]["coordinates"][0])
            if country := Country.objects.filter(name=country_name).first():
                data = {
                    "country": country,
                    "event_id": event_id,
                    "magnitude": magnitude,
                    "magnitude_type": magnitude_type,
                    "event_title": earthquake["properties"]["title"],
                    "event_place": earthquake["properties"]["place"],
                    "event_date": self.parse_timestamp(earthquake["properties"]["time"]),
                    "updated_at": self.parse_timestamp(earthquake["properties"]["updated"]),
                    "latitude": earthquake["geometry"]["coordinates"][1],
                    "longitude": earthquake["geometry"]["coordinates"][0],
                    "depth": earthquake["geometry"]["coordinates"][2],
                }
                # lets create corresponding database field
                Earthquake.objects.get_or_create(**data)
                all_data.append(data)

        # lets log the imported data as well
        file_name = f"{today}-earthquake-data.csv"
        with open(f"/tmp/{file_name}", "w", newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, header)
            dict_writer.writeheader()
            dict_writer.writerows(all_data)

        added = Earthquake.objects.count()
        logger.info(f"Added Earthquake data count {added}")
