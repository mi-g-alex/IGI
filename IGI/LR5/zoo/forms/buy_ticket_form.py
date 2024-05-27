import datetime

from django import forms
from django.utils import timezone

from zoo.models import Ticket, Price, Promo


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['date']

    promo = forms.CharField(label="Promo", required=False)
    date = forms.DateTimeField(widget=forms.SelectDateWidget())

    base_price = forms.ModelChoiceField(
        queryset=Price.objects.filter(is_addition=False),
        widget=forms.RadioSelect,
        required=True,
        label="Базовый билет"
    )

    additions = forms.ModelMultipleChoiceField(
        queryset=Price.objects.filter(is_addition=True),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Дополнения"
    )

    def clean_date(self):
        date = self.cleaned_data['date']
        now = datetime.datetime.now()
        if (date.year, date.month, date.day) < (now.year, now.month, now.day):
            raise forms.ValidationError("Can't bought to the past")
        return date

    def clean_promo(self):
        promo = self.cleaned_data['promo']
        now = timezone.now()
        res = Promo.objects.filter(name=promo, last_date__gte=now, first_date__lte=now).count()
        if promo != '':
            if res == 0:
                raise forms.ValidationError("Not found!")
        return promo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['base_price'].label_from_instance = self.label_from_instance
        self.fields['additions'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return f"{obj.name} - {obj.price}$."
