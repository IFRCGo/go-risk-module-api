from rest_framework import serializers

from ipc.models import (
    Country,
    GlobalDisplacement,
    ThinkHazardInformation
)



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


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
