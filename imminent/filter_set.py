import django_filters

from imminent.models import Earthquake, Adam
from common.models import HazardType


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

    class Meta:
        model = Adam
        fields = ()
