import datetime
import json
import logging

import pytz
import urllib3
from django.core.management.base import BaseCommand
from django.db import models
from django.utils import timezone
from sentry_sdk.crons import monitor

from common.models import HazardType
from imminent.models import Adam
from risk_module.sentry import SentryMonitor

logger = logging.getLogger(__name__)


def get_timezone_aware_datetime(iso_format_datetime) -> datetime.datetime:
    publish_date = datetime.datetime.fromisoformat(iso_format_datetime)
    if publish_date.tzinfo is None:
        publish_date = publish_date.replace(tzinfo=pytz.UTC)
    return publish_date


class Command(BaseCommand):
    help = "Import ADAM Cyclone Geojson"

    @staticmethod
    def adam_qs() -> models.QuerySet[Adam]:
        return Adam.objects.filter(hazard_type=HazardType.CYCLONE)

    @monitor(monitor_slug=SentryMonitor.UPDATE_ADAM_CYCLONE)
    def handle(self, **options):
        http = urllib3.PoolManager()

        # NOTE: Look for last 3 month (Longest cyclone in history at the time was 36 days)
        threshold_date = timezone.now() - datetime.timedelta(days=60)

        cyclone_events_qs = self.adam_qs().filter(publish_date__gte=threshold_date).values_list("event_id", flat=True).distinct()
        logger.info(f"Events to check: {cyclone_events_qs.count()}")
        for event_id in cyclone_events_qs:
            logger.info(f"Fetching event_id: {event_id}")
            cyclone_url = f"https://x8qclqysv7.execute-api.eu-west-1.amazonaws.com/dev/events/cyclones/{event_id}"
            response = http.request("GET", cyclone_url)
            data = response.data
            cyclone_data = json.loads(data)

            features_properties = cyclone_data["features"][0]["properties"]
            publish_date = get_timezone_aware_datetime(features_properties["published_at"])
            if not self.adam_qs().filter(event_id=event_id, publish_date__lt=publish_date).exists():
                logger.info("Nothing to update.....")
                continue

            resp = (
                self.adam_qs()
                .filter(event_id=event_id)
                .update(
                    title=features_properties["title"],
                    storm_position_geojson=cyclone_data,
                    publish_date=publish_date,
                    event_details=features_properties,
                )
            )
            logger.info(f"Updated {resp}")
