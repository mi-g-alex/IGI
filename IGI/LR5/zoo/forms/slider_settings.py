from django import forms
from zoo.models.Info import SliderSetitngs

class SliderSettingsForm(forms.ModelForm):
    class Meta:
        model = SliderSetitngs
        fields = '__all__'