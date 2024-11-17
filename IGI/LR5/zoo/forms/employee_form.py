from django import forms
from zoo.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'photo', 'info', 'phone', 'email']