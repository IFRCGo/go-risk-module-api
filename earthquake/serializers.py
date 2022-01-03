from rest_framework import serializers

from ipc.serializers import CountrySerializer

from earthquake.models import Earthquake


class EarthquakeSerializer(serializers.ModelSerializer):
    country_details = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = Earthquake
        fields = '__all__'
