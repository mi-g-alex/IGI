from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BUA
from django.contrib.auth.models import User

from .models import *
from .models.Info import About

# Register your models here.

models = (
    AnimalParameter, AnimalView, Animal, Country, AnimalFamily,
    Employee,
    FoodName, Food,
    PlaceQuarter, Place,
    Position,
    Ticket, Client, Comment,
    AdsBanners, Partners, About, New, Price, Promo, Vacancy, Term
)


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'


class ClientInline(admin.StackedInline):
    model = Client
    can_delete = False
    verbose_name_plural = 'client'


class UserAdmin(BUA):
    inlines = (EmployeeInline, ClientInline)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if hasattr(obj, 'courier_profile'):
            obj.is_staff = True
            obj.save()


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

for m in models:
    admin.site.register(m)
