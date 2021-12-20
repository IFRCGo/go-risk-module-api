import django_filters

from oddrin.models import (
    Idmc,
    InformRisk,
    IdmcSuddenOnset,
    InformRiskSeasonal,
    DisplacementData,
    GarHazard,
    PdcDisplacement
)
from oddrin.models import HazardType, Oddrin


class IdmcFilterSet(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='country', lookup_expr='icontains')
    iso3 = django_filters.CharFilter(field_name='iso3', lookup_expr='icontains')

    class Meta:
        model = Idmc
        fields = ()


class BaseFilterSet(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='country', lookup_expr='icontains')
    iso3 = django_filters.CharFilter(field_name='country__iso3', lookup_expr='icontains')
    hazard_type = django_filters.MultipleChoiceFilter(
        choices=HazardType.choices,
        widget=django_filters.widgets.CSVWidget,
    )


class InformRiskFilterSet(BaseFilterSet):
    class Meta:
        model = InformRisk
        fields = ()


class IdmcSuddenOnsetFilterSet(BaseFilterSet):
    class Meta:
        model = IdmcSuddenOnset
        fields = ()


class InfromRiskSeasonalFilterSet(BaseFilterSet):
    class Meta:
        model = InformRiskSeasonal
        fields = ()


class OddrinFilterSet(django_filters.FilterSet):
    iso3 = django_filters.CharFilter(field_name='iso3', lookup_expr='icontains')
    hazard_type = django_filters.MultipleChoiceFilter(
        choices=HazardType.choices,
        widget=django_filters.widgets.CSVWidget,
    )

    class Meta:
        model = Oddrin
        fields = ()


class DisplacementDataFilterSet(BaseFilterSet):
    class Meta:
        model = DisplacementData
        fields = ()


class GarHazardFilterSet(BaseFilterSet):
    class Meta:
        model = GarHazard
        fields = ()


class PdcDisplacemenFilterSet(django_filters.FilterSet):
    start_date__gte = django_filters.DateFilter(
        field_name='pdc__start_date',
        lookup_expr='gte',
    )
    end_date__lte = django_filters.DateFilter(
        field_name='pdc__end_date',
        lookup_expr='lte',
    )
    country = django_filters.CharFilter(field_name='country', lookup_expr='icontains')
    iso3 = django_filters.CharFilter(field_name='country__iso3', lookup_expr='icontains')
    hazard_type = django_filters.MultipleChoiceFilter(
        choices=HazardType.choices,
        widget=django_filters.widgets.CSVWidget,
    )

    class Meta:
        model = PdcDisplacement
        fields = ()
