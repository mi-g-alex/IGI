from django.contrib.auth.models import User as AdmUser
from django.db import models
from django.utils import timezone

from zoo.models.BaseModel import BaseModel
from zoo.models.Info import Price

from phonenumber_field.modelfields import PhoneNumberField


class Client(BaseModel):
    user = models.OneToOneField(AdmUser, on_delete=models.CASCADE, related_name='client')
    birthday = models.DateField()
    phone = PhoneNumberField()


class Ticket(BaseModel):
    date = models.DateTimeField(default=timezone.now)
    price = models.ManyToManyField(to=Price, related_query_name="sold_tickets")
    user = models.ForeignKey(to=Client, on_delete=models.CASCADE, related_query_name='tickets', default=None, null=True)
    paid = models.BooleanField(default=False)
    count = models.IntegerField(default=1)
    total_price = models.FloatField(default=0)


class Comment(BaseModel):
    text = models.TextField()
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Client, related_query_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return self.text + ' by ' + self.user.user.username
