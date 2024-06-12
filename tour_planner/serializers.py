from rest_framework import serializers

from tour_planner.models import District, WeatherUpdate


class WeatherUpdateSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name')
    district_bn_name = serializers.CharField(source='district.bn_name')
    lat = serializers.FloatField(source='district.lat')
    lon = serializers.FloatField(source='district.lon')

    class Meta:
        model = WeatherUpdate
        fields = '__all__'


class WeatherInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherUpdate
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    weather = WeatherInfoSerializer(many=True, read_only=True, source='weather_updates')
    division = serializers.CharField(source='division.name')

    class Meta:
        model = District
        fields = '__all__'
