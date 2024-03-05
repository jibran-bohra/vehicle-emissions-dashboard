from django.db import models

# Create your models here.

class ToyotaModels(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    vehicle_make = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Estimate(models.Model):
    id = models.CharField(primary_key=True,max_length=100)
    type = models.CharField(max_length=20)
    distance_value = models.FloatField()
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_year = models.PositiveIntegerField()
    vehicle_model_id = models.CharField(max_length=100)
    distance_unit = models.CharField(max_length=10)
    estimated_at = models.DateTimeField()
    carbon_g = models.PositiveIntegerField()
    carbon_lb = models.FloatField()
    carbon_kg = models.FloatField()
    carbon_mt = models.FloatField()

    def __str__(self):
        return f"{self.vehicle_make} {self.vehicle_model} - {self.vehicle_year}"

class APICallCounter(models.Model):
    call_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.call_count
    
