import datetime

from django.db import models

from zoo.models.BaseModel import BaseModel


class FoodName(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Food(BaseModel):
    food_name = models.ForeignKey(FoodName, on_delete=models.CASCADE)
    portion = models.FloatField(default=0.0)
    time = models.TimeField(default=datetime.time)

    def __str__(self):
        return self.food_name.name + ' ' + str(self.portion) + 'kg at ' + str(self.time)
