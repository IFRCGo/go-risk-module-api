from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from common.models import HazardType
from imminent.models import Adam
from risk_module.sentry import SentryMonitor


# TODO: Not used
# - This is used to update legacy data update_adam_alert_level
# This was one time to add color
# This is by another command
class Command(BaseCommand):
    help = "Update Adam Earthquake Alert Level"

    @monitor(monitor_slug=SentryMonitor.UPDATE_ADAM_ALERT_LEVEL)
    def handle(self, *args, **kwargs):
        adams = Adam.objects.filter(hazard_type=HazardType.EARTHQUAKE).only("id", "event_details")
        for adam in adams:
            if adam.event_details is None:
                continue

            mag = adam.event_details.get("mag")
            if mag is None:
                continue

            alert_level = None
            if mag < 6.2:
                alert_level = "Green"
            elif mag > 6 and mag <= 6.5:
                alert_level = "Orange"
            elif mag > 6.5:
                alert_level = "Red"

            if alert_level is None:
                continue

            adam.event_details["alert_level"] = alert_level
            adam.save(update_fields=["event_details"])
