import logging

import pandas as pd
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from common.models import Country, HazardType
from seasonal.models import GarProbabilistic

logger = logging.getLogger(__name__)


def parse_hazard_type(hazard_type):
    hazar_dict = {
        "Flood": HazardType.FLOOD,
        "Earthquake": HazardType.EARTHQUAKE,
        "Cyclone": HazardType.CYCLONE,
        "Epidemic": HazardType.EPIDEMIC,
        "Food Insecurity": HazardType.FOOD_INSECURITY,
        "Storm Surge": HazardType.STORM,
        "Drought": HazardType.DROUGHT,
        "Tsunami": HazardType.TSUNAMI,
        "Wind": HazardType.WIND,
    }
    return hazar_dict.get(hazard_type)


class Command(BaseCommand):
    help = "Import GarProbabilistic Data"

    def handle(self, *args, **options):
        countries_iso3 = Country.objects.values_list("iso3", flat=True)
        for iso3 in countries_iso3:
            iso = iso3.upper()
            url = f"https://www.preventionweb.net/english/hyogo/gar/2015/en/home/iso/{iso}.html"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "lxml")

            if len(soup.find_all("table")) > 0:
                tables = pd.read_html(response.content)
                if len(tables) > 3:
                    annual_probabilistic_table = tables[2]
                    annual_probabilistic_table = annual_probabilistic_table[:-1]
                    for row in annual_probabilistic_table.iterrows():
                        hazard_type = parse_hazard_type(row[1][0])
                        if hazard_type:
                            data = {
                                "country": Country.objects.filter(iso3__icontains=iso3).first(),
                                "hazard_type": hazard_type,
                                "absolute_loss_in_million": row[1][1] * 1000000,
                                "capital_stock_percentage": row[1][2],
                                "gfcf": row[1][3],
                                "social_exp": row[1][4],
                                "total_revenue": row[1][5],
                                "gross_saving": row[1][6],
                            }
                            GarProbabilistic.objects.create(**data)
