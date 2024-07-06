import urllib3
import logging
import datetime
import pytz
import json

from django.core.management.base import BaseCommand
from django.db import models
from django.utils import timezone
from sentry_sdk.crons import monitor

from risk_module.sentry import SentryMonitor
from common.models import HazardType
# from risk_module.managers import BulkUpdateManager
from imminent.models import Adam


logger = logging.getLogger(__name__)


def get_timezone_aware_datetime(iso_format_datetime) -> datetime.datetime:
    publish_date = datetime.datetime.fromisoformat(iso_format_datetime)
    if publish_date.tzinfo is None:
        publish_date = publish_date.replace(tzinfo=pytz.UTC)
    return publish_date


class AdamConfig:
    BASE_URL = "https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev"

    HazardTypeMap = {
        "Earthquake": HazardType.EARTHQUAKE,
        "Flood": HazardType.FLOOD,
        "Tropical Storm": HazardType.CYCLONE,
    }

    @classmethod
    def get_feed_url(cls, start_date: datetime.date, end_date: datetime.date):
        return (
            f"{cls.BASE_URL}/events/feed?start_date={start_date.isoformat()}&end_date={end_date.isoformat()}"
        )

    @classmethod
    def get_cyclone_url(cls, event_id):
        return f"{cls.BASE_URL}/events/cyclones/{event_id}"


# TODO: Just using feed should replace ./create_adam_exposure.py
class Command(BaseCommand):
    help = "Import ADAM Cyclone Geojson"

    @staticmethod
    def adam_qs() -> models.QuerySet[Adam]:
        return Adam.objects.filter(hazard_type=HazardType.CYCLONE)

    def full_sync(self):
        # TODO: Use async instead?
        http = urllib3.PoolManager()

        now = timezone.now() - datetime.timedelta(days=60)  # XXX: Look for last 3 month
        cyclone_events_qs = self.adam_qs().filter(publish_date__gte=now).values_list('event_id', flat=True).distinct()
        logger.info(f"Events to check: {cyclone_events_qs.count()}")
        for event_id in cyclone_events_qs:
            logger.info(f"Fetching event_id: {event_id}")
            cyclone_url = AdamConfig.get_cyclone_url(event_id)
            response = http.request("GET", cyclone_url)
            data = response.data
            cyclone_data = json.loads(data)

            publish_date = get_timezone_aware_datetime(cyclone_data["features"][0]["properties"]["published_at"])
            if not self.adam_qs().filter(event_id=event_id, publish_date__lt=publish_date).exists():
                logger.info('Nothing to update.....')
                continue

            resp = self.adam_qs().filter(event_id=event_id).update(
                storm_position_geojson=cyclone_data,
                publish_date=publish_date,
                event_details=cyclone_data["features"][0]["properties"],
            )
            logger.info(f'Updated {resp}')

    @monitor(monitor_slug=SentryMonitor.UPDATE_ADAM_CYCLONE)
    def handle(self, **options):
        return self.full_sync()

    """
    NOTE: Another way to do it as well. Using Feed isn't showing all cyclone updates,
     but maybe we can use cyclone endpoint instead but only update changed events
    def recent_sync(self):
        \"""
        Docs: https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/docs#/Event%20Feed/Recent_Events_events_feed_get
        Usages: https://github.com/OCHA-DAP/hdx-scraper-wfp-adam/blob/main/run.py
        \"""
        bulk_mgr = BulkUpdateManager(["storm_position_geojson", "publish_date", "event_details"], chunk_size=100)

        http = urllib3.PoolManager()

        now = timezone.now().date()
        recent_feed_url = AdamConfig.get_feed_url(
            # TODO: Store the last day state
            now - datetime.timedelta(days=30),  # Look for last 30 days
            now,
        )
        recent_feeds_data = json.loads(
            http.request("GET", recent_feed_url).data,
        )

        for recent_feed in recent_feeds_data:
            hazard_type_raw = recent_feed["eventType"]
            hazard_type = AdamConfig.HazardTypeMap.get(hazard_type_raw)
            if hazard_type != HazardType.CYCLONE:
                logger.debug(f"Unkown hazard_type: {hazard_type_raw}")
                continue

            cyclone_url = recent_feed["eventDetails"]
            cyclone_event_publish_date = get_timezone_aware_datetime(recent_feed["pubDate"])
            event_id = cyclone_url.split('/')[-1]

            cyclone_event = self.adam_qs().filter(event_id=event_id).first()
            if cyclone_event is None:
                logger.debug("No cyclone_event in the database")
                continue

            print('-' * 22, event_id)
            print('cyclone_event_publish_date:', recent_feed["pubDate"], cyclone_event_publish_date)
            print(cyclone_event.publish_date)
            print(cyclone_event.publish_date <= cyclone_event_publish_date)

            if cyclone_event.publish_date <= cyclone_event_publish_date:
                logger.info(f"Database already has the latest data: {cyclone_event.publish_date} <= {cyclone_event_publish_date}")
                continue

            logger.info("Looks good..............................")
            cyclone_data = json.loads(
                http.request("GET", cyclone_url).data,
            )

            cyclone_event.storm_position_geojson = cyclone_data
            cyclone_event.publish_date = get_timezone_aware_datetime(
                cyclone_data["features"][0]["properties"]["published_at"]
            )
            cyclone_event.event_details = cyclone_data["features"][0]["properties"]
            logger.info(cyclone_event.publish_date)
            bulk_mgr.add(cyclone_event)

        bulk_mgr.done()
        logger.info(bulk_mgr.summary())
    """
