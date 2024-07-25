import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand

from common.models import Country, HazardType
from seasonal.models import InformRiskSeasonal, RiskScore


class Command(BaseCommand):
    """
    This class creates data calculating the risk score
    """

    def add_arguments(self, parser):
        parser.add_argument("file1")
        parser.add_argument("file2")

    def map_hazard_type(self, hazard_type):
        if hazard_type == "DR":
            return HazardType.DROUGHT
        elif hazard_type == "FL":
            return HazardType.FLOOD
        elif hazard_type == "TC":
            return HazardType.CYCLONE
        return

    def handle(self, **options):
        file1 = options.get("file1")
        file2 = options.get("file2")
        # lets import the data from the inform seasonal data
        inform_score_dataframe = pd.DataFrame(
            list(
                InformRiskSeasonal.objects.values(
                    "country__name",
                    "country__iso3",
                    "hazard_type",
                    "january",
                    "february",
                    "march",
                    "april",
                    "may",
                    "june",
                    "july",
                    "august",
                    "september",
                    "october",
                    "november",
                    "december",
                )
            )
        )
        inform_score_dataframe.rename({"country__iso3": "ISO3"}, axis=1, inplace=True)
        # Filter Out Inform IndicatorId
        df1 = inform_score_dataframe
        df1["ISO3"] = df1["ISO3"].str.upper()
        # latest inform score data
        df2 = pd.read_excel(file1, sheet_name="INFORM Risk 2024 (a-z)", skiprows=(0, 2), usecols="A, B, S, AE", engine="openpyxl")
        df2.rename(
            {"VULNERABILITY": "Vulnerability", "LACK OF COPING CAPACITY": "LCC"},
            axis=1,
            inplace=True,
        )
        # population data
        pop = pd.read_excel(file2, sheet_name="Estimates", skiprows=range(1, 16), usecols="C, F, K, L")
        new_header = pop.iloc[0]  # grab the first row for the header
        df3 = pop[1:]  # take the data less the header row
        df3.columns = new_header  # set the header row as the df header
        population_dataframe = df3[df3.Year == 2020]
        population_dataframe.rename(
            {"ISO3 Alpha-code": "ISO3", "Total Population, as of 1 January (thousands)": "Population_in_thousands"},
            axis=1,
            inplace=True,
        )
        # for population dataframe add `iso3`
        # provided csv lacks iso3
        #  Loading go region grouping
        regional_dataframe = pd.DataFrame(
            list(Country.objects.filter(independent=True, is_deprecated=False).values("iso3", "name", "region__name"))
        )
        regional_dataframe.rename({"iso3": "ISO3", "region__name": "Region"}, axis=1, inplace=True)
        regional_dataframe["ISO3"] = regional_dataframe["ISO3"].str.upper()
        df1["ISO3"] = df1["ISO3"].str.upper()

        # meging dataframes
        df32 = pd.merge(df1, df2, how="left", on="ISO3")
        df32region = pd.merge(df32, regional_dataframe, how="inner", on="ISO3")
        df4 = pd.merge(df32region, population_dataframe, how="inner", on="ISO3")
        df4["Risk-Rel-JAN"] = df4.january
        df4["Risk-Rel-FEB"] = df4.february
        df4["Risk-Rel-MAR"] = df4.march
        df4["Risk-Rel-APR"] = df4.april
        df4["Risk-Rel-MAY"] = df4.may
        df4["Risk-Rel-JUN"] = df4.june
        df4["Risk-Rel-JUL"] = df4.july
        df4["Risk-Rel-AUG"] = df4.august
        df4["Risk-Rel-SEP"] = df4.september
        df4["Risk-Rel-OCT"] = df4.october
        df4["Risk-Rel-NOV"] = df4.november
        df4["Risk-Rel-DEC"] = df4.december

        filtered_df = df4[df4["hazard_type"].notnull()]
        for index, row in filtered_df.iterrows():
            yearly_sum = np.sum(
                [
                    row["Risk-Rel-JAN"],
                    row["Risk-Rel-FEB"],
                    row["Risk-Rel-MAR"],
                    row["Risk-Rel-APR"],
                    row["Risk-Rel-MAY"],
                    row["Risk-Rel-JUN"],
                    row["Risk-Rel-JUL"],
                    row["Risk-Rel-AUG"],
                    row["Risk-Rel-SEP"],
                    row["Risk-Rel-OCT"],
                    row["Risk-Rel-NOV"],
                    row["Risk-Rel-DEC"],
                ]
            )
            risk_score_data = {
                "country": Country.objects.filter(
                    iso3__icontains=row["ISO3"],
                    iso3__isnull=False,
                    record_type__isnull=False,
                    record_type=Country.CountryType.COUNTRY,
                ).first(),
                "january": row["Risk-Rel-JAN"],
                "february": row["Risk-Rel-FEB"],
                "march": row["Risk-Rel-MAR"],
                "april": row["Risk-Rel-APR"],
                "may": row["Risk-Rel-MAY"],
                "june": row["Risk-Rel-JUN"],
                "july": row["Risk-Rel-JUL"],
                "august": row["Risk-Rel-AUG"],
                "september": row["Risk-Rel-SEP"],
                "october": row["Risk-Rel-OCT"],
                "november": row["Risk-Rel-NOV"],
                "december": row["Risk-Rel-DEC"],
                "yearly_sum": yearly_sum,
                "hazard_type": self.map_hazard_type(row["hazard_type"]),
                "lcc": row["LCC"],
                "population_in_thousands": row["Population_in_thousands"],
                "vulnerability": row["Vulnerability"],
            }
            RiskScore.objects.create(**risk_score_data)
