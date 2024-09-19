import datetime

from zoo.models import Position
from zoo.models.BaseModel import BaseModel
from django.db import models
from django.utils import timezone

class About(BaseModel):
    info = models.TextField()
    logo = models.ImageField(upload_to='photos/about/')
    video = models.FileField(upload_to='photos/about/')
    year_history = models.TextField()
    certificate = models.TextField()

    def __str__(self):
        return "About"


class New(BaseModel):
    title = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos/news/', default=None, null=True)
    text = models.TextField()

    def __str__(self):
        return self.title


class Vacancy(BaseModel):
    salary = models.FloatField()
    position = models.ForeignKey(Position, related_query_name="vacancies", on_delete=models.CASCADE)

    def __str__(self):
        return self.position.name


class Term(BaseModel):
    title = models.CharField(max_length=50)
    info = models.TextField()

    def __str__(self):
        return self.title


class Promo(BaseModel):
    name = models.CharField(max_length=50)
    discount = models.FloatField()
    first_date = models.DateTimeField(default=timezone.now)
    last_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Price(BaseModel):
    name = models.CharField(max_length=50)
    is_addition = models.BooleanField(default=False)
    price = models.FloatField()

    def __str__(self):
        return self.name
