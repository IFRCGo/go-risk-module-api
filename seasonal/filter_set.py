
import django_filters

from common.models import HazardType
from seasonal.models import (
    PossibleEarlyActions,
    PublishReport,
    RiskScore,
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
    hazard_type = django_filters.MultipleChoiceFilter(
        choices=HazardType.choices,
        widget=django_filters.widgets.CSVWidget,
    )
    sectors = django_filters.CharFilter(
        field_name='sectors__name',
        lookup_expr='icontains',
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


class RiskScoreFilterSet(django_filters.FilterSet):
    iso3 = django_filters.CharFilter(
        lookup_expr='icontains',
        field_name='country__iso3'
    )
    region = django_filters.NumberFilter(
        lookup_expr='icontains',
        field_name='country__region__name'
    )

    class Meta:
        model = RiskScore
        fields = ()
