import pandas as pd

from django.core.management.base import BaseCommand

from imminent.models import Adam
from common.models import HazardType


class Command(BaseCommand):
    help = "Import exposure data from excel file"

    def handle(self, *args, **kwargs):
        # get the execel file from the event_details for cyclone

        cyclones = (
            Adam.objects.filter(hazard_type=HazardType.CYCLONE)
            .order_by("-publish_date", "country")
            .distinct("country", "publish_date")
        )
        for cyclone in cyclones:
            excel_file = cyclone.event_details["url"]["population"]
            if excel_file:
                try:
                    file = pd.read_excel(excel_file, skiprows=12, engine="openpyxl")
                    new_dataframe = pd.DataFrame(file)
                    if cyclone.country:
                        country = cyclone.country.name
                        df_by_total = new_dataframe[new_dataframe["ADM0_NAME"] == f"{country}  - TOT"]
                        df_by_country = new_dataframe[new_dataframe["ADM0_NAME"] == country]
                        if len(df_by_total) > 0:
                            country1_df = df_by_total
                        elif len(df_by_country) > 0:
                            country1_df = df_by_country
                        else:
                            country1_df = []
                        if len(country1_df) > 0:
                            country1_speed = country1_df.iloc[:, 4:].values.tolist()
                            if len(country1_speed[0]) == 4:
                                speed_60 = country1_speed[0][0]
                                speed_90 = country1_speed[0][1]
                                speed_120 = country1_speed[0][2]
                            elif len(country1_speed[0]) == 3:
                                speed_60 = country1_speed[0][0]
                                speed_90 = country1_speed[0][1]
                                speed_120 = None
                            elif len(country1_speed[0]) == 2:
                                speed_60 = country1_speed[0][0]
                                speed_90 = None
                                speed_120 = None

                            exposure_dict = {
                                "exposure_60km/h": speed_60,
                                "exposure_90km/h": speed_90,
                                "exposure_120km/h": speed_120,
                            }
                            cyclone.population_exposure = exposure_dict
                            cyclone.save(update_fields=["population_exposure"])
                except ValueError:
                    pass
