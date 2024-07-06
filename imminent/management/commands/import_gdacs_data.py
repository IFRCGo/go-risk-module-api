import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand
from sentry_sdk.crons import monitor

from risk_module.sentry import SentryMonitor
from imminent.models import GDACS
from common.models import Country, HazardType


class Command(BaseCommand):
    help = "Import Active Hazards From GDACS"

    def import_hazard_data(self, hazard_type, hazard_type_str):
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        url = f"https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventlist={hazard_type}&fromDate={yesterday}&toDate={today}&alertlevel=Green;Orange;Red"  # noqa: E501
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Error querying GDACS data at {url}"))
            return

        response_data = response.json()

        for old_data in response_data["features"]:
            event_id = old_data["properties"]["eventid"]

            if GDACS.objects.filter(hazard_id=event_id).exists():
                continue

            location = old_data["bbox"]
            data = {
                "hazard_id": event_id,
                "hazard_name": old_data["properties"]["eventname"] or old_data["properties"]["htmldescription"],
                "start_date": old_data["properties"]["fromdate"],
                "end_date": old_data["properties"]["todate"],
                "alert_level": old_data["properties"]["alertlevel"],
                "country": Country.objects.filter(iso3__iexact=old_data["properties"]["iso3"]).first(),
                "event_details": old_data["properties"],
                "hazard_type": hazard_type_str,
                "latitude": location[1],
                "longitude": location[0],
            }

            scrape_url = f"https://www.gdacs.org/report.aspx?eventid={event_id}&eventtype={hazard_type_str}"
            try:
                tables = pd.read_html(scrape_url)
                displacement_data = tables[0].replace({np.nan: None}).to_dict()
                data["population_exposure"] = {}
                if hazard_type_str == "EQ":
                    data["population_exposure"]["exposed_population"] = displacement_data.get(1, {}).get(5)
                elif hazard_type_str == "TC":
                    data["population_exposure"]["exposed_population"] = displacement_data.get(1, {}).get("Exposed population")
                elif hazard_type_str == "FL":
                    data["population_exposure"]["death"] = (
                        int(displacement_data.get(1, {}).get(1))
                        if displacement_data.get(1, {}).get(1) != "-"
                        else None
                    )
                    data["population_exposure"]["displaced"] = (
                        int(displacement_data.get(1, {}).get(2))
                        if displacement_data.get(1, {}).get(2) != "-"
                        else None
                    )
                elif hazard_type_str == "DR":
                    data["population_exposure"]["impact"] = displacement_data.get("Impact:")
                elif hazard_type_str == "WF":
                    data["population_exposure"]["people_affected"] = displacement_data.get(1, {}).get(4)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error scraping data from {scrape_url}: {e}"))

            footprint_url = old_data["properties"]["url"]["geometry"]
            footprint_response = requests.get(footprint_url)

            if footprint_response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Error querying Footprint data at {footprint_url}"))
                continue

            footprint_response_data = footprint_response.json()
            data["footprint_geojson"] = footprint_response_data

            GDACS.objects.create(**data)

    @monitor(monitor_slug=SentryMonitor.IMPORT_GDACS_DATA)
    def handle(self, *args, **kwargs):
        self.import_hazard_data("EQ", HazardType.EARTHQUAKE)
        self.import_hazard_data("TC", HazardType.CYCLONE)
        self.import_hazard_data("FL", HazardType.FLOOD)
        self.import_hazard_data("DR", HazardType.DROUGHT)
        self.import_hazard_data("WF", HazardType.WILDFIRE)
