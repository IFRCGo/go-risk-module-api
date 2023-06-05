import requests
import logging
import pandas as pd
import urllib
import numpy as np
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from imminent.models import GDACS
from common.models import HazardType, Country


logger = logging.getLogger()


class Command(BaseCommand):
    # NOTE: Source GDACS
    help = "Import Active Hazards From Gdacs"

    def handle(self, *args, **kwargs):
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        # Import for earthquake
        url = f"https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventlist=EQ&fromDate={yesterday}&toDate={today}&alertlevel=Green;Orange;Red"
        response = requests.get(url)
        if response.status_code == 200:
            error_log = f"Error querying GDACS data at {url}"
            logger.error(error_log)
            logger.error(response.content)
            response_data = response.json()
            for old_data in response_data["features"]:
                # basics data to be stored as
                episode_id = old_data["properties"]["episodeid"]
                event_id = old_data["properties"]["eventid"]
                location = old_data["bbox"]
                if GDACS.objects.filter(hazard_id=event_id).exists():
                    continue
                else:
                    data = {
                        "hazard_id": old_data["properties"]["eventid"],
                        "hazard_name": old_data["properties"]["eventname"]
                        if old_data["properties"]["eventname"] != ""
                        else old_data["properties"]["htmldescription"],
                        "start_date": old_data["properties"]["fromdate"],
                        "end_date": old_data["properties"]["todate"],
                        "alert_level": old_data["properties"]["alertlevel"],
                        "country": Country.objects.filter(iso3=old_data["properties"]["iso3"].lower()).first(),
                        "event_details": old_data["properties"],
                        "hazard_type": HazardType.EARTHQUAKE,
                        "latitude": location[1],
                        "longitude": location[0],
                    }
                scrape_url = f"https://www.gdacs.org/report.aspx?eventid={event_id}&episodeid={episode_id}&eventtype=EQ"

                # for population exposre data lets read from the  table
                try:
                    tables = pd.read_html(scrape_url)
                except urllib.error.URLError:
                    pass
                displacement_data = tables[0]
                displacement_data = displacement_data.replace({np.nan: None})
                data.update(
                    {
                        "population_exposure": {
                            "exposed_population": displacement_data[1].iloc[5]
                            if displacement_data[1].iloc[5] != "NaN"
                            else None,
                        }
                    }
                )
                footprint_url = old_data["properties"]["url"]["geometry"]
                try:
                    footprint_response = requests.get(footprint_url)
                except requests.exceptions.ConnectionError:
                    continue
                if response.status_code != 200:
                    error_log = f"Error querying PDC data at {url}"
                    logger.error(error_log)
                    logger.error(footprint_response.content)
                footprint_response_data = footprint_response.json()
                data.update(
                    {
                        "footprint_geojson": footprint_response_data,
                    }
                )
                if GDACS.objects.filter(hazard_id=data["hazard_id"]).exists():
                    continue
                else:
                    GDACS.objects.create(**data)

        # # # Import Tropical Cyclone
        cyclone_url = f"https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventlist=TC&fromDate={yesterday}&toDate={today}&alertlevel=Green;Orange;Red"
        response = requests.get(cyclone_url)
        if response.status_code == 200:
            error_log = f"Error querying GDACS data at {cyclone_url}"
            logger.error(error_log)
            logger.error(response.content)
            response_data = response.json()
            for old_data in response_data["features"]:
                episode_id = old_data["properties"]["episodeid"]
                event_id = old_data["properties"]["eventid"]
                location = old_data["bbox"]
                if GDACS.objects.filter(hazard_id=old_data["properties"]["eventid"]).exists():
                    continue
                else:
                    data = {
                        "hazard_id": old_data["properties"]["eventid"],
                        "hazard_name": old_data["properties"]["eventname"]
                        if old_data["properties"]["eventname"] != ""
                        else old_data["properties"]["htmldescription"],
                        "start_date": old_data["properties"]["fromdate"],
                        "end_date": old_data["properties"]["todate"],
                        "alert_level": old_data["properties"]["alertlevel"],
                        "country": Country.objects.filter(iso3__exact=old_data["properties"]["iso3"].lower()).first(),
                        "event_details": old_data["properties"],
                        "hazard_type": HazardType.CYCLONE,
                        "latitude": location[1],
                        "longitude": location[0],
                    }
                    scrape_url = f"https://www.gdacs.org/report.aspx?eventid={event_id}&episodeid={episode_id}&eventtype=TC"

                    # for population exposre data lets read from the  table
                    tables = pd.read_html(scrape_url)
                    displacement_data = tables[0]
                    data.update(
                        {
                            "population_exposure": {
                                "exposed_population": displacement_data[1].iloc[4],
                            }
                        }
                    )
                    footprint_url = old_data["properties"]["url"]["geometry"]
                    footprint_response = requests.get(footprint_url)
                    if response.status_code != 200:
                        error_log = f"Error querying Footprint data at {footprint_url}"
                        logger.error(error_log)
                        logger.error(footprint_response.content)
                    footprint_response_data = footprint_response.json()
                    data.update({"footprint_geojson": footprint_response_data})
                    GDACS.objects.create(**data)

        # Import Flood data
        flood_url = f"https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventlist=FL&fromDate={yesterday}&toDate={today}&alertlevel=Green;Orange;Red"
        response = requests.get(flood_url)
        if response.status_code == 200:
            error_log = f"Error querying GDACS data at {flood_url}"
            logger.error(error_log)
            # logger.error(response.content)
            response_data = response.json()
            for old_data in response_data["features"]:
                episode_id = old_data["properties"]["episodeid"]
                event_id = old_data["properties"]["eventid"]
                location = old_data["bbox"]
                if GDACS.objects.filter(hazard_id=event_id).exists():
                    continue
                else:
                    data = {
                        "hazard_id": old_data["properties"]["eventid"],
                        "hazard_name": old_data["properties"]["eventname"]
                        if old_data["properties"]["eventname"] != ""
                        else old_data["properties"]["htmldescription"],
                        "start_date": old_data["properties"]["fromdate"],
                        "end_date": old_data["properties"]["todate"],
                        "alert_level": old_data["properties"]["alertlevel"],
                        "country": Country.objects.filter(iso3=old_data["properties"]["iso3"].lower()).first(),
                        "event_details": old_data["properties"],
                        "hazard_type": HazardType.FLOOD,
                        "latitude": location[1],
                        "longitude": location[0],
                    }
                scrape_url = f"https://www.gdacs.org/report.aspx?eventid={event_id}&episodeid={episode_id}&eventtype=FL"
                # for population exposre data lets read from the  table
                tables = pd.read_html(scrape_url)
                displacement_data = tables[0]
                data.update(
                    {
                        "population_exposure": {
                            "death": int(displacement_data[1].iloc[1]) if displacement_data[1].iloc[1] != "-" else None,
                            "displaced": int(displacement_data[1].iloc[2]) if displacement_data[1].iloc[2] != "-" else None,
                        }
                    }
                )
                footprint_url = old_data["properties"]["url"]["geometry"]
                footprint_response = requests.get(footprint_url)
                if response.status_code == 200:
                    error_log = f"Error querying Footprint data at {footprint_url}"
                    logger.error(error_log)
                    logger.error(footprint_response.content)
                    footprint_response_data = footprint_response.json()
                    data.update({"footprint_geojson": footprint_response_data})
                    GDACS.objects.create(**data)

        # # Import Drought Data
        drought_url = f"https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventlist=DR&fromDate={yesterday}&toDate={today}&alertlevel=Green;Orange;Red"
        response = requests.get(drought_url)
        if response.status_code == 200:
            error_log = f"Error querying GDACS data at {drought_url}"
            logger.error(error_log)
            logger.error(response.content)
            response_data = response.json()
            for old_data in response_data["features"]:
                episode_id = old_data["properties"]["episodeid"]
                event_id = old_data["properties"]["eventid"]
                location = old_data["bbox"]
                if GDACS.objects.filter(hazard_id=event_id).exists():
                    continue
                else:
                    data = {
                        "hazard_id": old_data["properties"]["eventid"],
                        "hazard_name": old_data["properties"]["eventname"]
                        if old_data["properties"]["eventname"] != ""
                        else old_data["properties"]["htmldescription"],
                        "start_date": old_data["properties"]["fromdate"],
                        "end_date": old_data["properties"]["todate"],
                        "alert_level": old_data["properties"]["alertlevel"],
                        "country": Country.objects.filter(iso3=old_data["properties"]["iso3"].lower()).first(),
                        "event_details": old_data["properties"],
                        "hazard_type": HazardType.DROUGHT,
                        "latitude": location[1],
                        "longitude": location[0],
                    }
                    scrape_url = f"https://www.gdacs.org/report.aspx?eventid={event_id}&episodeid={episode_id}&eventtype=DR"

                    # for population exposre data lets read from the  table
                    tables = pd.read_html(scrape_url)
                    displacement_data = tables[0]
                    # print(displacement_data)
                    # print(displacement_data.iloc[0])
                    # data.update(
                    #     {
                    #         'population_exposure': displacement_data[1].iloc[5] if displacement_data[1].iloc[2] != '-' or '' else None
                    #     }
                    # )
                    footprint_url = old_data["properties"]["url"]["geometry"]
                    footprint_response = requests.get(footprint_url)
                    if response.status_code != 200:
                        error_log = f"Error querying Footprint data at {footprint_url}"
                        logger.error(error_log)
                        logger.error(footprint_response.content)
                    footprint_response_data = footprint_response.json()
                    data.update({"footprint_geojson": footprint_response_data})
                    GDACS.objects.create(**data)

        # # Import Wildfire Data
        wildfire_url = f"https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?eventlist=WF&fromDate={yesterday}&toDate={today}&alertlevel=Green;Orange;Red"
        response = requests.get(wildfire_url)
        if response.status_code == 200:
            error_log = f"Error querying GDACS data at {wildfire_url}"
            logger.error(error_log)
            logger.error(response.content)
            response_data = response.json()
            for old_data in response_data["features"]:
                episode_id = old_data["properties"]["episodeid"]
                event_id = old_data["properties"]["eventid"]
                location = old_data["bbox"]
                if GDACS.objects.filter(hazard_id=event_id).exists():
                    continue
                else:
                    data = {
                        "hazard_id": old_data["properties"]["eventid"],
                        "hazard_name": old_data["properties"]["eventname"]
                        if old_data["properties"]["eventname"] != ""
                        else old_data["properties"]["htmldescription"],
                        "start_date": old_data["properties"]["fromdate"],
                        "end_date": old_data["properties"]["todate"],
                        "alert_level": old_data["properties"]["alertlevel"],
                        "country": Country.objects.filter(iso3=old_data["properties"]["iso3"].lower()).first(),
                        "event_details": old_data["properties"],
                        "hazard_type": HazardType.WILDFIRE,
                        "latitude": location[1],
                        "longitude": location[0],
                    }
                    scrape_url = f"https://www.gdacs.org/report.aspx?eventid={event_id}&episodeid={episode_id}&eventtype=WF"

                    # for population exposre data lets read from the  table
                    tables = pd.read_html(scrape_url)
                    displacement_data = tables[0]
                    data.update(
                        {
                            "population_exposure": {
                                "people_affected": displacement_data[1].iloc[4]
                                if displacement_data[1].iloc[4] != "-" or ""
                                else None
                            }
                        }
                    )
                    footprint_url = old_data["properties"]["url"]["geometry"]
                    footprint_response = requests.get(footprint_url)
                    if response.status_code != 200:
                        error_log = f"Error querying Footprint data at {footprint_url}"
                        logger.error(error_log)
                        logger.error(footprint_response.content)
                    footprint_response_data = footprint_response.json()
                    data.update({"footprint_geojson": footprint_response_data})
