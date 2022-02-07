from rest_framework import serializers

from seasonal.models import (
    GlobalDisplacement,
    ThinkHazardInformation,
    Idmc,
    IdmcSuddenOnset,
    InformRisk,
    InformRiskSeasonal,
    DisplacementData,
    GarHazardDisplacement
)
from common.serializers import CountrySerializer


class GlobalDisplacementSerializer(serializers.ModelSerializer):
    country_details = CountrySerializer(source='country', read_only=True)
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    estimation_type_display = serializers.CharField(source='get_estimation_type_display')

    class Meta:
        model = GlobalDisplacement
        fields = '__all__'


class ThinkHazardInformationSerializer(serializers.ModelSerializer):
    country_details = CountrySerializer(source='country', read_only=True)
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    hazard_level_display = serializers.CharField(source='get_hazard_level_display')

    class Meta:
        model = ThinkHazardInformation
        fields = '__all__'


class IdmcSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    country_details = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = Idmc
        fields = '__all__'


class InformRiskSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    country_details = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = InformRisk
        fields = '__all__'


class IdmcSuddenOnsetSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    country_details = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = IdmcSuddenOnset
        fields = '__all__'


class InformRiskSeasonalSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    country_details = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = InformRiskSeasonal
        fields = '__all__'


class DisplacementDataSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    country_details = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = DisplacementData
        fields = '__all__'


class GarHazardDisplacementSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    country_details = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = GarHazardDisplacement
        fields = '__all__'
