from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from rest_framework.response import Response
from tour_planner.models import District, WeatherUpdate
from tour_planner.serializers import DistrictSerializer, WeatherUpdateSerializer
import pandas as pd
from retry_requests import retry

from tour_planner.open_metro import load_api_data, load_daily_data


# Create your views here.


def index(request):
    return render(request, 'index.html')


class TestView(APIView):
    permission_classes = []

    def get(self, request):

        # save daily data on database 
        districts = District.objects.all()
        for district in districts:

            weather_data = load_api_data(district.lat, district.lon)
            print(weather_data)
            daily_dataframe = load_daily_data(weather_data)
            print(daily_dataframe)

            for index, row in daily_dataframe.iterrows():
                # save data on database
                print(row['date'], row['temperature_2m_max'], row['temperature_2m_min'], row['rain_sum'])
                if WeatherUpdate.objects.filter(district=district, date=row['date']).exists():
                    continue
                if not row['rain_sum'] or pd.isna(row['rain_sum']):
                    row['rain_sum'] = 0
                avg_temp = (row['temperature_2m_max'] + row['temperature_2m_min']) / 2
                WeatherUpdate.objects.create(district=district, date=row['date'], max_temp=row['temperature_2m_max'],
                                             min_temp=row['temperature_2m_min'], avg_temp=avg_temp,
                                             rain=row['rain_sum'])

        return Response({'msg': daily_dataframe})


class DistrictViewset(ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def get_queryset(self):
        if self.request.query_params.get('search'):
            search = self.request.query_params.get('search')
            return District.objects.filter(Q(name__icontains=search) | Q(bn_name__icontains=search))
        return District.objects.all()


class WeatherViewset(ModelViewSet):
    queryset = WeatherUpdate.objects.all()
    serializer_class = WeatherUpdateSerializer

    def get_queryset(self):
        if self.request.query_params.get('search'):
            search = self.request.query_params.get('search')
            if search == 'coolest':
                return WeatherUpdate.objects.order_by('min_temp','avg_temp').all()[:1]
            if search == 'hottest':
                return WeatherUpdate.objects.order_by('-max_temp','-avg_temp').all()[:1]
        return WeatherUpdate.objects.order_by('avg_temp').all()
