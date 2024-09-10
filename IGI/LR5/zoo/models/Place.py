from django.db import models

from zoo.models.BaseModel import BaseModel


class PlaceQuarter(BaseModel):
    name = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.name


class Place(BaseModel):
    name = models.CharField(max_length=50)
    number = models.SmallIntegerField()
    has_swimming = models.BooleanField()
    has_heating = models.BooleanField()
    square = models.FloatField()
    quarter = models.ForeignKey(PlaceQuarter, on_delete=models.CASCADE, related_query_name="places")

    def __str__(self):
        return self.name
