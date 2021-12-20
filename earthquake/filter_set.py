import django_filters

from earthquake.models import Earthquake


class EarthquakeFilterSet(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='country', lookup_expr='icontains')
    event_date__lte = django_filters.DateFilter(field_name='event_date', lookup_expr='lte')
    event_date__gte = django_filters.DateFilter(field_name='event_date', lookup_expr='gte')

    class Meta:
        model = Earthquake
        fields = ()
