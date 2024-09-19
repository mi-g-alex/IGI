from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from zoo.forms.buy_ticket_form import TicketForm
from zoo.forms.login_form import LoginForm
from zoo.forms.registration_form import UserRegistrationForm
from zoo.models import Ticket, Price, Promo, Client
import datetime


class TicketFormTest(TestCase):

    def setUp(self):
        self.base_price = Price.objects.create(name="Adult", price=20.0, is_addition=False)
        self.addition1 = Price.objects.create(name="Safari Tour", price=5.0, is_addition=True)
        self.addition2 = Price.objects.create(name="Animal Feeding", price=10.0, is_addition=True)

        self.promo = Promo.objects.create(name="DISCOUNT10", discount=10,
                                          first_date=timezone.now() - datetime.timedelta(days=1),
                                          last_date=timezone.now() + datetime.timedelta(days=1))

    def test_ticket_form_valid_data(self):
        form_data = {
            'date': timezone.now() + datetime.timedelta(days=1),
            'promo': 'DISCOUNT10',
            'base_price': self.base_price.id,
            'additions': [self.addition1.id, self.addition2.id],
        }
        form = TicketForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ticket_form_invalid_past_date(self):
        form_data = {
            'date': timezone.now() - datetime.timedelta(days=1),
            'promo': '',
            'base_price': self.base_price.id,
            'additions': [self.addition1.id],
        }
        form = TicketForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertEqual(form.errors['date'], ["Can't bought to the past"])

    def test_ticket_form_invalid_promo(self):
        form_data = {
            'date': timezone.now() + datetime.timedelta(days=1),
            'promo': 'INVALIDPROMO',
            'base_price': self.base_price.id,
            'additions': [self.addition1.id],
        }
        form = TicketForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('promo', form.errors)
        self.assertEqual(form.errors['promo'], ["Not found!"])

    def test_ticket_form_empty_promo(self):
        form_data = {
            'date': timezone.now() + datetime.timedelta(days=1),
            'promo': '',
            'base_price': self.base_price.id,
            'additions': [self.addition1.id],
        }
        form = TicketForm(data=form_data)
        self.assertTrue(form.is_valid())


class UserRegistrationFormTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'phone': '+375291234567',
            'birthday': '2000-01-01',
            'password1': 'strongpassword',
            'password2': 'strongpassword'
        }

    def test_form_valid_data(self):
        form = UserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_phone(self):
        invalid_data = self.valid_data.copy()
        invalid_data['phone'] = '1234567890'
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_form_invalid_birthday(self):
        invalid_data = self.valid_data.copy()
        invalid_data['birthday'] = (timezone.now() - datetime.timedelta(days=365 * 14)).strftime('%Y-%m-%d')
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('birthday', form.errors)

    def test_form_password_mismatch(self):
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'differentpassword'
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_save(self):
        form = UserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.client.phone, '+375291234567')

    def test_form_duplicate_username(self):
        User.objects.create_user(username='testuser', password='password')
        form = UserRegistrationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class LoginFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_form_valid_data(self):
        form_data = {'username': 'testuser', 'password': 'password'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_empty_password(self):
        form_data = {'username': 'testuser', 'password': ''}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_form_widget_attributes(self):
        form = LoginForm()
        self.assertEqual(form.fields['username'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password'].widget.attrs['class'], 'form-control')
