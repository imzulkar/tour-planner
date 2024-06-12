from rest_framework import serializers

from tour_planner.models import District, WeatherUpdate, TouristPlace


class TourPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristPlace
        fields = '__all__'


class WeatherUpdateSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name')
    district_bn_name = serializers.CharField(source='district.bn_name')
    lat = serializers.FloatField(source='district.lat')
    lon = serializers.FloatField(source='district.lon')
    min_temp = serializers.DecimalField(max_digits=5, decimal_places=2)
    max_temp = serializers.DecimalField(max_digits=5, decimal_places=2)
    avg_temp = serializers.DecimalField(max_digits=5, decimal_places=2)
    rain = serializers.DecimalField(max_digits=5, decimal_places=2)
    tour_places = TourPlaceSerializer(source='district.tourist_places', many=True, read_only=True)

    class Meta:
        model = WeatherUpdate
        fields = '__all__'


class WeatherInfoSerializer(serializers.ModelSerializer):
    min_temp = serializers.DecimalField(max_digits=5, decimal_places=2)
    max_temp = serializers.DecimalField(max_digits=5, decimal_places=2)
    avg_temp = serializers.DecimalField(max_digits=5, decimal_places=2)
    rain = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = WeatherUpdate
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    weather = WeatherInfoSerializer(many=True, read_only=True, source='weather_updates')
    division = serializers.CharField(source='division.name')
    division_density = serializers.CharField(source='division.density')
    division_area = serializers.CharField(source='division.area')
    division_population = serializers.CharField(source='division.population')

    class Meta:
        model = District
        fields = '__all__'
