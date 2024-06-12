from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('districts', views.DistrictViewset, basename='districts')
router.register('weather', views.WeatherViewset, basename='weather')
urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.TestView.as_view(), name='test'),

]+router.urls
