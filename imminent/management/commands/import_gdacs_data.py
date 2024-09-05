import logging
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pytz
import requests
from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from common.models import Country, HazardType
from common.utils import logging_context, logging_response_context
from imminent.models import GDACS
from risk_module.sentry import SentryMonitor

logger = logging.getLogger(__name__)


def get_timezone_aware_datetime(iso_format_datetime) -> datetime:
    publish_date = datetime.fromisoformat(iso_format_datetime)
    if publish_date.tzinfo is None:
        publish_date = publish_date.replace(tzinfo=pytz.UTC)
    return publish_date


class Command(BaseCommand):
    help = "Import Active Hazards From GDACS"

    def scrape_population_exposure_data(self, event_id: int, hazard_type_str: str):
        url = f"https://www.gdacs.org/report.aspx?eventid={event_id}&eventtype={hazard_type_str}"
        population_exposure = {}
        try:
            tables = pd.read_html(url)
            displacement_data = tables[0].replace({np.nan: None}).to_dict()
            if hazard_type_str == "EQ":
                population_exposure["exposed_population"] = displacement_data.get(1, {}).get(5)
            elif hazard_type_str == "TC":
                population_exposure["exposed_population"] = displacement_data.get(1, {}).get("Exposed population")
            elif hazard_type_str == "FL":
                population_exposure["death"] = (
                    int(displacement_data.get(1, {}).get(1)) if displacement_data.get(1, {}).get(1) != "-" else None
                )
                population_exposure["displaced"] = (
                    int(displacement_data.get(1, {}).get(2)) if displacement_data.get(1, {}).get(2) != "-" else None
                )
            elif hazard_type_str == "DR":
                population_exposure["impact"] = displacement_data.get("Impact:")
            elif hazard_type_str == "WF":
                population_exposure["people_affected"] = displacement_data.get(1, {}).get(4)
        except Exception:
            logger.error(
                "Error scraping data",
                extra=logging_context(dict(url=url)),
                exc_info=True,
            )
        return population_exposure

    def import_hazard_data(self, hazard_type, hazard_type_str):
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        url = f"https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventlist={hazard_type}&fromDate={yesterday}&toDate={today}&alertlevel=Green;Orange;Red"  # noqa: E501
        response = requests.get(url)

        if response.status_code == 204:
            # No Content from server
            return

        # Log other errors
        if response.status_code != 200:
            logger.error(
                "Error querying GDACS data",
                extra=logging_response_context(response),
            )
            return

        response_data = response.json()

        for old_data in response_data["features"]:
            event_id = old_data["properties"]["eventid"]
            episode_id = old_data["properties"]["episodeid"]

            if GDACS.objects.filter(hazard_id=event_id, episode_id=episode_id).exists():
                continue

            location = old_data["bbox"]
            data = {
                "episode_id": episode_id,
                "hazard_name": old_data["properties"]["eventname"] or old_data["properties"]["htmldescription"],
                "start_date": get_timezone_aware_datetime(old_data["properties"]["fromdate"]),
                "end_date": get_timezone_aware_datetime(old_data["properties"]["todate"]),
                "alert_level": old_data["properties"]["alertlevel"],
                "country": Country.objects.filter(iso3__iexact=old_data["properties"]["iso3"]).first(),
                "event_details": old_data["properties"],
                "hazard_type": hazard_type_str,
                "latitude": location[1],
                "longitude": location[0],
            }

            data["population_exposure"] = self.scrape_population_exposure_data(event_id, hazard_type_str)

            footprint_url = old_data["properties"]["url"]["geometry"]
            if hazard_type == HazardType.CYCLONE:
                footprint_url = f"https://www.gdacs.org/contentdata/resources/{hazard_type_str}/{event_id}/geojson_{event_id}_{episode_id}.geojson"  # noqa: E501

            footprint_response = requests.get(footprint_url)
            if footprint_response.status_code != 200:
                logger.error(
                    "Error querying Footprint data",
                    extra=logging_response_context(response),
                )
                continue

            footprint_response_data = footprint_response.json()
            data["footprint_geojson"] = footprint_response_data

            GDACS.objects.update_or_create(hazard_id=event_id, **data)

    @monitor(monitor_slug=SentryMonitor.IMPORT_GDACS_DATA)
    def handle(self, **_):
        self.import_hazard_data("EQ", HazardType.EARTHQUAKE)
        self.import_hazard_data("TC", HazardType.CYCLONE)
        self.import_hazard_data("FL", HazardType.FLOOD)
        self.import_hazard_data("DR", HazardType.DROUGHT)
        self.import_hazard_data("WF", HazardType.WILDFIRE)
