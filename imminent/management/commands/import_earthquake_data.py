import requests
import datetime
import logging
import csv
from dateutil.relativedelta import relativedelta

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from django.core.management.base import BaseCommand
from django.utils import timezone
from sentry_sdk.crons import monitor

from risk_module.sentry import SentryMonitor
from common.models import Country

from imminent.models import Earthquake

logger = logging.getLogger()


# XXX: Not used right now
class Command(BaseCommand):
    help = "Import Earthquake geo-locations from external api"

    def parse_timestamp(self, timestamp):
        # NOTE: all timestamp are in millisecond and with timezone `utc`
        return timezone.make_aware(datetime.datetime.utcfromtimestamp(timestamp / 1000))

    def get_country(self, latitude, longitude):
        geolocator = Nominatim(user_agent="risk_module_earthquake")
        reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)
        location = reverse((latitude, longitude), language="en", exactly_one=True)
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
        url = (
            f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={seven_days_before}&endtime={today}"
        )
        response = requests.get(url)
        if response.status_code != 200:
            error_log = f"Error querying earthquake data at {url}"
            logger.error(error_log)
            logger.error(response.content)
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
            country = self.get_country(earthquake["geometry"]["coordinates"][1], earthquake["geometry"]["coordinates"][0])
            if Country.objects.filter(name=country).exists():
                data = {
                    "event_id": earthquake["id"],
                    "event_title": earthquake["properties"]["title"],
                    "event_place": earthquake["properties"]["place"],
                    "event_date": self.parse_timestamp(earthquake["properties"]["time"]),
                    "updated_at": self.parse_timestamp(earthquake["properties"]["updated"]),
                    "latitude": earthquake["geometry"]["coordinates"][1],
                    "longitude": earthquake["geometry"]["coordinates"][0],
                    "depth": earthquake["geometry"]["coordinates"][2],
                    "magnitude": earthquake["properties"]["mag"],
                    "magnitude_type": earthquake["properties"]["magType"],
                    "country": Country.objects.filter(name=country).first(),
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
