import datetime
import logging

import pytz
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from sentry_sdk.crons import monitor

from common.models import HazardType
from common.utils import logging_response_context
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

    @monitor(monitor_slug=SentryMonitor.UPDATE_ADAM_CYCLONE)
    def handle(self, **_):
        http_session = requests.Session()

        # NOTE: Look for last 3 month (Longest cyclone in history at the time was 36 days)
        threshold_date = timezone.now() - datetime.timedelta(days=60)

        base_adam_qs = Adam.objects.filter(hazard_type=HazardType.CYCLONE)
        cyclone_events_qs = base_adam_qs.filter(publish_date__gte=threshold_date).values_list("event_id", flat=True).distinct()

        logger.info(f"Events to check: {cyclone_events_qs.count()}")
        for event_id in cyclone_events_qs:
            logger.info(f"Fetching event_id: {event_id}")

            response = http_session.get(f"{settings.WFP_ADAM}/events/cyclones/{event_id}")
            if response.status_code != 200:
                logger.error(
                    "Error querying Cyclone data",
                    extra=logging_response_context(response),
                )
                continue
            cyclone_data = response.json()

            features_properties = cyclone_data["features"][0]["properties"]
            publish_date = get_timezone_aware_datetime(features_properties["published_at"])
            if not base_adam_qs.filter(event_id=event_id, publish_date__lt=publish_date).exists():
                logger.info("Nothing to update.....")
                continue

            resp = base_adam_qs.filter(event_id=event_id).update(
                title=features_properties["title"],
                storm_position_geojson=cyclone_data,
                publish_date=publish_date,
                event_details=features_properties,
            )
            logger.info(f"Updated {resp}")
