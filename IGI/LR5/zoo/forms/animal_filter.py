from django import forms

from zoo.models import AnimalFamily, Country, Place, AnimalView


class AnimalFilterForm(forms.Form):
    SORT_CHOICES = [
        ('default', 'Default'),
        ('name_asc', 'Name (A-Z)'),
        ('name_desc', 'Name (Z-A)'),
    ]
    name = forms.CharField(max_length=50, required=False)
    family = forms.ModelChoiceField(queryset=AnimalFamily.objects.all(), required=False)
    countries = forms.ModelMultipleChoiceField(queryset=Country.objects.all(), required=False)
    place = forms.ModelChoiceField(queryset=Place.objects.all(), required=False)
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)
