from django import forms

from zoo.models import AnimalFamily, Country, Place, AnimalView, FoodName


class SuperUserAnimalFilterForm(forms.Form):
    name = forms.CharField(max_length=50, required=False)
    view = forms.ModelChoiceField(queryset=AnimalView.objects.all(), required=False)
    place = forms.ModelChoiceField(queryset=Place.objects.all(), required=False)
    food = forms.ModelMultipleChoiceField(queryset=FoodName.objects.all(), required=False)
    recently = forms.BooleanField(required=False, label="Recently (last 180 days)")
