import requests
import logging

from django.core.management.base import BaseCommand

from common.models import HazardType, Country
from common.utils import logging_response_context
from imminent.models import GWIS

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import Active Hazards From GWIS"

    def handle(self, *args, **kwargs):
        # Get all the countries with iso3 codes that are not deprecated and independent
        country_iso3 = list(Country.objects.filter(is_deprecated=False, independent=True).values_list("iso3", flat=True))

        for year in range(2024, 2025):
            for iso3 in country_iso3:
                if iso3:
                    self.import_monthly_data(iso3, year)
                    self.import_cumulative_data(iso3, year)

    def import_monthly_data(self, iso3, year):
        url = f"https://api2.effis.emergency.copernicus.eu/statistics/v2/dsr/monthly?country={iso3.upper()}&year={year}"
        response = requests.get(url, verify=False)

        if response.status_code != 200:
            logger.error(
                "Error querying GWIS data - Monthly Data",
                extra=logging_response_context(response),
            )
            return

        response_data = response.json()
        monthly_response = response_data.get("dsrmonthly", [])

        for month in monthly_response:
            self.create_gwis_entry(iso3, month, year, GWIS.DSRTYPE.MONTHLY)

    def import_cumulative_data(self, iso3, year):
        url = f"https://api2.effis.emergency.copernicus.eu/statistics/v2/dsr/cumulative?country={iso3.upper()}&year={year}"
        response = requests.get(url, verify=False)

        if response.status_code != 200:
            logger.error(
                "Error querying GWIS data - Cumulative data",
                extra=logging_response_context(response),
            )
            return

        response_data = response.json()
        cumulative_response = response_data.get("dsrcumulative", [])

        for month in cumulative_response:
            self.create_gwis_entry(iso3, month, year, GWIS.DSRTYPE.CUMULATIVE)

    def create_gwis_entry(self, iso3, data, year, dsr_type):
        country = Country.objects.filter(iso3=iso3).first()

        if not country:
            return

        gwis_data = {
            "country": country,
            "month": data["month"],
            "dsr": data["dsr"],
            "dsr_min": data["dsr_min"],
            "dsr_avg": data["dsr_avg"],
            "dsr_max": data["dsr_max"],
            "dsr_type": dsr_type,
            "year": year,
            "hazard_type": HazardType.WILDFIRE,
        }

        GWIS.objects.get_or_create(**gwis_data)
