from django.db import models
from django.utils import timezone

from zoo.models.BaseModel import BaseModel
from zoo.models.Employee import Employee
from zoo.models.Food import Food
from zoo.models.Place import Place


class AnimalFamily(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AnimalView(BaseModel):
    name = models.CharField(max_length=50)
    family = models.ForeignKey(AnimalFamily, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Country(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AnimalParameter(BaseModel):
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        return str(self.length) + "-" + str(self.width) + "-" + str(self.height) + "-" + str(self.weight)


class Animal(BaseModel):
    name = models.CharField(max_length=50)
    receipt_date = models.DateTimeField(default=timezone.now)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, related_query_name="animals", null=True, related_name="animals")
    birthday = models.DateTimeField(default=timezone.now)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, related_query_name="news", null=True)
    food = models.ManyToManyField(Food, related_query_name="animals")
    facts = models.TextField()
    counties = models.ManyToManyField(Country, related_query_name="animals")
    view = models.ForeignKey(AnimalView, on_delete=models.SET_NULL, related_query_name="animals", null=True)
    photo = models.ImageField(upload_to='photos/animals/')
    parameters = models.OneToOneField(AnimalParameter, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name + ' ' + self.place.name
