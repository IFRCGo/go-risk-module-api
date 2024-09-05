import datetime
import typing

from django.utils import timezone

from common.models import Country


def parse_timestamp(timestamp):
    # NOTE: all timestamp are in millisecond and with timezone `utc`
    return timezone.make_aware(
        # FIXME: Using deprecated function
        datetime.datetime.utcfromtimestamp(int(timestamp) / 1000)
    )


class CountryQuery:
    def __init__(self):
        self._countries: typing.List[Country] = list(Country.objects.all())
        self._countries_iso3_map: typing.Dict[str, Country] = {country.iso3.lower(): country for country in self._countries}

    def get_by_iso3(self, iso3: str) -> typing.Optional[Country]:
        return self._countries_iso3_map.get(iso3.lower())


def chunk_list(lst: typing.List[typing.Any], n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
