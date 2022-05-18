
import django_filters

from seasonal.models import (
    PossibleEarlyActions,
    PublishReport
)


class PossibleEarlyActionsFilterSet(django_filters.FilterSet):
    iso3 = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='country__iso3'
    )
    region = django_filters.NumberFilter(
        lookup_expr='icontains',
        field_name='country__region__name'
    )

    class Meta:
        model = PossibleEarlyActions
        fields = ()


class PublishReportFilterSet(django_filters.FilterSet):
    iso3 = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='program__country__iso3'
    )
    region = django_filters.NumberFilter(
        lookup_expr='icontains',
        field_name='program__country__region__name'
    )

    class Meta:
        model = PublishReport
        fields = ()
