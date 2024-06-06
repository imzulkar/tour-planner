from django.db import models

# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=100)
    total_district = models.IntegerField(default=0)
    total_upazila = models.IntegerField(default=0)
    area = models.FloatField(default=0.0)
    population = models.IntegerField(default=0)
    density = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=100)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='districts')
    def __str__(self):
        return self.name


class WeatherUpdate(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='weather_updates')
    date = models.DateField()
    min_temp = models.FloatField(default=0.0)
    max_temp = models.FloatField(default=0.0)
    avg_temp = models.FloatField(default=0.0)
    rain = models.FloatField(default=0.0)
    def __str__(self):
        return self.district.name + ' ' + str(self.date)

class TouristPlace(models.Model):
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='tourist_places')
    description = models.TextField()
    def __str__(self):
        return self.name