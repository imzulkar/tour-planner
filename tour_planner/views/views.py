from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from tour_planner.models import District, WeatherUpdate
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
                WeatherUpdate.objects.create(district=district, date=row['date'], max_temp=row['temperature_2m_max'], min_temp=row['temperature_2m_min'], rain=row['rain_sum'])
            
            
        return Response({'msg': daily_dataframe})