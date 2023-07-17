import pandas as pd

from seasonal.models import ThinkHazardCountry


def create_think_hazard(file):
    data_file = pd.read_csv(file, sep=";")
    countries = [
        ThinkHazardCountry(country_id=data["ADM0_CODE"], name=data["ADM0_NAME"], iso3=data["ISO3166_a3"])
        for i, data in data_file.iterrows()
    ]
    ThinkHazardCountry.objects.bulk_create(countries)
