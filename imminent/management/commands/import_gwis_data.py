import requests
import logging


from django.core.management.base import BaseCommand

from imminent.models import GWIS
from common.models import HazardType, Country


logger = logging.getLogger()


class Command(BaseCommand):
    # NOTE: Source GDACS
    help = "Import Active Hazards From Gdacs"

    def handle(self, *args, **kwargs):
        # Import for earthquake
        # get all the country
        country_iso3 = list(Country.objects.filter(is_deprecated=False, independent=True).values_list("iso3", flat=True))
        for year in range(2003, 2024):
            for iso3 in country_iso3:
                url = f"https://api2.effis.emergency.copernicus.eu/statistics/v2/dsr/monthly?country={iso3.upper()}&year={year}"
                response = requests.get(url, verify=False)
                if response.status_code != 200:
                    error_log = f"Error querying GWIS data at {url}"
                    logger.error(error_log)
                    logger.error(response.content)
                # get the monthly_data
                response = response.json()
                monthly_response = response["dsrmonthly"]
                if monthly_response:
                    for month in monthly_response:
                        monthly_data = {
                            "country": Country.objects.filter(iso3=iso3).first(),
                            "month": month["month"],
                            "dsr": month["dsr"],
                            "dsr_min": month["dsr_min"],
                            "dsr_avg": month["dsr_avg"],
                            "dsr_max": month["dsr_max"],
                            "dsr_type": GWIS.DSRTYPE.MONTHLY,
                            "year": year,
                            "hazard_type": HazardType.WILDFIRE,
                        }
                        GWIS.objects.create(**monthly_data)
                cummulative_response = response["dsrcumulative"]
                if cummulative_response:
                    for month in cummulative_response:
                        cummulative_data = {
                            "country": Country.objects.filter(iso3=iso3).first(),
                            "month": month["month"],
                            "dsr": month["dsr"],
                            "dsr_min": month["dsr_min"],
                            "dsr_avg": month["dsr_avg"],
                            "dsr_max": month["dsr_max"],
                            "dsr_type": GWIS.DSRTYPE.CUMMULATIVE,
                            "year": year,
                            "hazard_type": HazardType.WILDFIRE,
                        }
                        GWIS.objects.create(**cummulative_data)
