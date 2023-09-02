import django_filters

from imminent.models import Earthquake, Adam, Pdc, GDACS, MeteoSwissAgg, GWIS
from common.models import (
    HazardType,
    Country,
    Region,
)


class EarthquakeFilterSet(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name="country", lookup_expr="icontains")
    event_date__lte = django_filters.DateFilter(field_name="event_date", lookup_expr="lte")
    event_date__gte = django_filters.DateFilter(field_name="event_date", lookup_expr="gte")

    class Meta:
        model = Earthquake
        fields = ()


class AdamFilterSet(django_filters.FilterSet):
    hazard_type = django_filters.MultipleChoiceFilter(
        choices=HazardType.choices,
        widget=django_filters.widgets.CSVWidget,
    )
    country = django_filters.ModelMultipleChoiceFilter(
        queryset=Country.objects.all(),
    )
    iso3 = django_filters.CharFilter(field_name="country__iso3", lookup_expr="icontains")
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(), field_name="country__region", label="region"
    )

    class Meta:
        model = Adam
        fields = ()

    @property
    def qs(self):
        qs = super().qs
        return qs.distinct('event_id')


class PdcFilterSet(django_filters.FilterSet):
    iso3 = django_filters.CharFilter(field_name="pdcdisplacement__country__iso3", lookup_expr="icontains", label="iso3")
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(), field_name="pdcdisplacement__country__region", label="region"
    )

    class Meta:
        model = Pdc
        fields = ()


class GDACSFilterSet(django_filters.FilterSet):
    iso3 = django_filters.CharFilter(field_name="country__iso3", lookup_expr="icontains", label="iso3")
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(), field_name="country__region", label="region"
    )

    class Meta:
        model = GDACS
        fields = ()


class MeteoSwissAggFilterSet(django_filters.FilterSet):
    iso3 = django_filters.CharFilter(field_name="country__iso3", lookup_expr="icontains", label="iso3")
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(), field_name="country__region", label="region"
    )

    class Meta:
        model = MeteoSwissAgg
        fields = ()


class GWISFilterSet(django_filters.FilterSet):
    iso3 = django_filters.CharFilter(field_name="country__iso3", lookup_expr="icontains", label="iso3")
    region = django_filters.ModelMultipleChoiceFilter(
        queryset=Region.objects.all(), field_name="country__region", label="region"
    )
    year = django_filters.CharFilter(field_name="year", lookup_expr="icontains", label="year")
    dsr_type = django_filters.MultipleChoiceFilter(
        choices=GWIS.DSRTYPE.choices,
        widget=django_filters.widgets.CSVWidget,
    )

    class Meta:
        model = GWIS
        fields = ()
