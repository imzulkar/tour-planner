from datetime import datetime

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
            date = self.request.query_params.get('date')
            return District.objects.filter(Q(name__icontains=search) | Q(bn_name__icontains=search) | Q())
        return District.objects.all()


class WeatherViewset(ModelViewSet):
    queryset = WeatherUpdate.objects.all()
    serializer_class = WeatherUpdateSerializer

    def get_queryset(self):

        data = WeatherUpdate.objects.all()

        search = self.request.query_params.get('search')
        date = self.request.query_params.get('date', '')
        min_temp = self.request.query_params.get('min_temp', 0)
        max_temp = self.request.query_params.get('max_temp', 100)
        if search or date or (min_temp and max_temp):
            if search and search == 'coolest':
                data = WeatherUpdate.objects.order_by('min_temp', 'avg_temp').all()

            if search and search == 'hottest':
                data = WeatherUpdate.objects.order_by('max_temp', '-avg_temp').all()
            if date != "":
                query_date = datetime.strptime(date, '%Y-%m-%d').date()
                data = data.filter(date=query_date)

            # print(data)
            if min_temp != "" and max_temp != "":
                return data.filter(Q(min_temp__gte=min_temp, max_temp__lte=max_temp))[:10]
            return data[:1]
        return data.order_by('-avg_temp')
