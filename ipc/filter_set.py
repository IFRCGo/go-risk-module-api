import django_filters

from ipc.models import GlobalDisplacement, EstimationType, ThinkHazardInformation
from oddrin.models import HazardType


class GlobalDisplacementFilterSet(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='country', lookup_expr='icontains')
    iso3 = django_filters.CharFilter(field_name='country__iso3', lookup_expr='icontains')
    hazard_type = django_filters.MultipleChoiceFilter(
        choices=HazardType.choices,
        widget=django_filters.widgets.CSVWidget,
    )
    estimation_type = django_filters.MultipleChoiceFilter(
        choices=EstimationType.choices,
        widget=django_filters.widgets.CSVWidget,
    )

    class Meta:
        model = GlobalDisplacement
        fields = ()


class ThinkHazardInformationFilterSet(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='country', lookup_expr='icontains')
    iso3 = django_filters.CharFilter(field_name='country__iso3', lookup_expr='icontains')
    hazard_type = django_filters.MultipleChoiceFilter(
        choices=HazardType.choices,
        widget=django_filters.widgets.CSVWidget,
    )

    class Meta:
        model = ThinkHazardInformation
        fields = ()
