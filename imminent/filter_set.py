import django_filters

from imminent.models import Earthquake, Adam
from common.models import HazardType, Country


class EarthquakeFilterSet(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='country', lookup_expr='icontains')
    event_date__lte = django_filters.DateFilter(field_name='event_date', lookup_expr='lte')
    event_date__gte = django_filters.DateFilter(field_name='event_date', lookup_expr='gte')

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
    iso3 = django_filters.CharFilter(
        field_name='country__iso3',
        lookup_expr='icontains'
    )

    class Meta:
        model = Adam
        fields = ()
