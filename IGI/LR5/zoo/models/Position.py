from django.db import models

from zoo.models.BaseModel import BaseModel


class Position(BaseModel):
    name = models.CharField(max_length=50)
    info = models.TextField()

    def __str__(self):
        return self.name
