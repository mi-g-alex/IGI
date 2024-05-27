import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from zoo.models import Client


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username')
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(label='Phone number')
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'birthday', 'password1', 'password2')

    def clean_birthday(self):
        value = self.cleaned_data['birthday']
        now = datetime.datetime.now()
        age = now.year - value.year
        if (now.month, now.day) < (value.month, value.day):
            age -= 1
        if age < 18:
            raise forms.ValidationError("Пользователи должны быть совершенно летними")
        return value

    def clean_phone(self):
        pattern = re.compile(r'^\+375(29|25|44|33)\d{7}$')
        phone = self.cleaned_data['phone']
        if not pattern.match(phone):
            raise ValidationError('Номер телефона должен быть введен в формате: "+375xxxxxxxxx".')
        return phone

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_username(self):
        return self.cleaned_data["username"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
            client = Client(
                user=user,
                phone=self.cleaned_data['phone'],
                birthday=self.cleaned_data['birthday'],
            )
            client.save()
        return user
