from rest_framework import serializers

from common.models import Country, Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    region_details = RegionSerializer(source='region', read_only=True)

    class Meta:
        model = Country
        fields = '__all__'
