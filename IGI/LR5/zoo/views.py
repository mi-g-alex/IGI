import logging

import matplotlib.pyplot as plt
import io
import urllib, base64

import requests
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LoginView
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404

from zoo.forms.animal_filter import AnimalFilterForm
from zoo.forms.buy_ticket_form import TicketForm
from zoo.forms.comment_form import CommentForm
from zoo.forms.login_form import LoginForm
from zoo.forms.registration_form import UserRegistrationForm

from django.contrib import messages

from zoo.forms.superuser_animal_filter import SuperUserAnimalFilterForm
from zoo.models import New, Term, Vacancy, Promo, Comment, Ticket, Price, Animal, Employee, Place, FoodName
from zoo.models.Info import About

logger = logging.getLogger(__name__)


def index(request):
    new = New.objects.last()

    response = requests.get('https://catfact.ninja/fact')
    fact = response.json()["fact"]

    logger.info("Visit index page")
    return render(request, 'main_page/index.html', {'new': new, 'fact': fact})


def about(request):
    logger.info("Visit about page")
    about_data = About.objects.last()
    text = about_data.info
    logo = about_data.logo
    video = about_data.video
    year_history = about_data.year_history
    return render(request, 'main_page/about.html',
                  {'text': text, 'logo': logo, 'video': video, 'year_history': year_history})


def certificate(request):
    view = About.objects.last().certificate
    response = render(
        request,
        "main_page/cert.html",
        context={'view': view}
    )
    response['X-Frame-Options'] = 'SAMEORIGIN'
    return response


def news(request):
    logger.info("Visit news page")
    all_news = New.objects.all()
    print(all_news[0].title)
    return render(request, 'main_page/news.html', context={'all_news': all_news})


def news_detail(request, pk):
    logger.info(f"Visit ${pk} new page")
    news_item = get_object_or_404(New, pk=pk)
    return render(request, 'main_page/news_details.html', {'news_item': news_item})


def terms(request):
    logger.info("Visit terms page")
    all_terms = Term.objects.all()
    return render(request, 'main_page/terms.html', {'terms': all_terms})


def vacancy(request):
    logger.info("Visit vacancy page")
    all_vacancies = Vacancy.objects.all()
    return render(request, 'main_page/vacancy.html', {'vacancies': all_vacancies})


def policy(request):
    logger.info("Visit policy page")
    return render(request, 'main_page/policy.html')


@login_required()
def promo(request):
    logger.info("Visit promo page")
    if not request.user.is_staff:
        now = timezone.now()
        archive_promo = Promo.objects.filter(last_date__lt=now).all().order_by("last_date")
        future_promo = Promo.objects.filter(first_date__gt=now).all().order_by("last_date")
        active_promo = Promo.objects.filter(last_date__gte=now, first_date__lte=now).all().order_by("last_date")
        return render(request, 'client/promo.html',
                      {
                          'future_promos': future_promo,
                          'active_promos': active_promo,
                          'archive_promos': archive_promo,
                      }
                      )
    else:
        logger.info("Access for staff denied!")
        return redirect("zoo:home_page")


def reviews(request):
    logger.info("Visit review page")
    all_reviews = Comment.objects.all()
    return render(request, 'main_page/reviews.html', {'reviews': all_reviews})


def register(request):
    if request.user.__class__ is not AnonymousUser:
        return redirect("zoo:profile")
    logger.info("Visit register page")
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.clean_username()
            messages.success(request, f'{username}')
            return redirect('zoo:home_page')
    else:
        form = UserRegistrationForm(request.POST)
    return render(request, 'auth/registration.html', {'form': form})


class Login(LoginView):
    authentication_form = LoginForm
    template_name = 'auth/login.html'
    redirect_authenticated_user = True


def my_logout(request):
    logger.info("Logout")
    logout(request)
    return redirect('zoo:auth_login')


@login_required
def profile(request):
    if not request.user.is_staff:
        return render(request, 'client/account.html', {'client': request.user.client})
    else:
        return redirect('zoo:home_page')


@login_required
def create_comment(request):
    logger.info("Create comment")
    if not request.user.is_staff:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user.client
                comment.save()
                return redirect('zoo:reviews_page')
        else:
            form = CommentForm(request.POST)
        return render(request, 'client/create_review.html', {'form': form})
    else:
        return redirect("zoo:home_page")


@login_required
def buy_ticket(request):
    logger.info("Buy ticket")
    client = request.user.client
    if client is None:
        return redirect("zoo:profile")

    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            base_price = form.cleaned_data['base_price']
            additions = form.cleaned_data['additions']
            promo = form.clean_promo()
            now = timezone.now()
            obj = Promo.objects.filter(name=promo, last_date__gte=now, first_date__lte=now).first()
            total_price = base_price.price + sum(addition.price for addition in additions)
            if obj is not Promo.DoesNotExist and obj is not None:
                total_price *= (1 - obj.discount / 100)
            ticket = Ticket(date=form.cleaned_data['date'], user=client, total_price=total_price)
            ticket.save()
            ticket.price.add(base_price)
            ticket.price.add(*additions)

            return redirect('zoo:cart')

    form = TicketForm(request.POST)

    return render(request, 'client/buy_ticket.html', {'form': form})


@login_required
def my_cart(request):
    client = request.user.client
    if client is None:
        return redirect("zoo:profile")

    if request.method == "POST":
        ticket_id = request.POST.get('ticket_id')
        action = request.POST.get('action')

        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.total_price /= ticket.count
        if action == 'increase':
            ticket.count += 1
        elif action == 'decrease':
            ticket.count -= 1
        ticket.total_price *= ticket.count
        ticket.save()
        if action == 'delete' or ticket.count <= 0:
            ticket.delete()
        return redirect('zoo:cart')

    tickets = Ticket.objects.filter(user=client, paid=False).all().order_by("date").reverse()

    return render(request, 'client/cart.html', {'tickets': tickets})


@login_required
def confirm_pay(request):
    client = request.user.client
    if client is None:
        return redirect("zoo:profile")

    tickets = Ticket.objects.filter(user=client, paid=False).all()

    if request.method == "POST":
        card = request.POST.get('card_number')
        expiration_date = request.POST.get('expiration_date')
        cvv = request.POST.get('cvv')

        for i in tickets:
            i.paid = True
            i.save()

        return redirect("zoo:my_tickets")

    sum_of_pay = 0
    for q in tickets:
        sum_of_pay += q.total_price

    return render(request, 'client/confirm_pay.html', {'total_price': sum_of_pay})


@login_required
def my_tickets(request):
    logger.info("Visit my tickets page")
    client = request.user.client
    if client is None:
        return redirect("zoo:profile")

    tickets = Ticket.objects.filter(user=client, paid=True).all().order_by("date").reverse()
    return render(request, 'client/my_tickets.html', {'tickets': tickets})


@staff_member_required()
def my_animals(request):
    logger.info("Visit my animals page")
    employee = request.user.employee
    print(employee)
    if employee is Employee.DoesNotExist:
        return redirect("zoo:profile")

    animals = Animal.objects.filter(employee=employee).all()
    return render(request, 'employee/my_animals.html', context={'animals': animals})


@staff_member_required()
def animal_detail(request, pk):
    logger.info("Visit animal details page")
    print(request.user)
    employee = None
    if not request.user.is_superuser:
        employee = request.user.employee

        if employee is Employee.DoesNotExist:
            return redirect("zoo:profile")

    try:
        item = Animal.objects.get(pk=pk)
        if not request.user.is_superuser and item.employee.pk != employee.pk:
            return redirect("zoo:my_animals ")
        else:
            return render(request, 'employee/my_animal_detail.html', {'animal': item})

    except Animal.DoesNotExist:
        if request.user.is_superuser:
            return redirect("zoo:superuser_all_animals")
        else:
            return redirect("zoo:my_animals")


def animal_list(request):
    animals = Animal.objects.all()
    form = AnimalFilterForm(request.GET or None)

    if form.is_valid():
        if form.cleaned_data['name']:
            animals = animals.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data['family']:
            animals = animals.filter(view__family=form.cleaned_data['family'])
        if form.cleaned_data['countries']:
            animals = animals.filter(counties__in=form.cleaned_data['countries']).distinct()
        if form.cleaned_data['place']:
            animals = animals.filter(place=form.cleaned_data['place']).distinct()
        if form.cleaned_data['sort_by']:
            if form.cleaned_data['sort_by'] == 'name_asc':
                animals = animals.order_by('name')
            elif form.cleaned_data['sort_by'] == 'name_desc':
                animals = animals.order_by('-name')

    context = {
        'form': form,
        'animals': animals
    }

    return render(request, 'main_page/animal_list.html', context)


@staff_member_required()
def super_user_animal_list(request):
    if not request.user.is_superuser:
        return redirect("zoo:my_animals")

    animals = Animal.objects.all()
    form = SuperUserAnimalFilterForm(request.GET or None)

    if form.is_valid():
        if form.cleaned_data['name']:
            animals = animals.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data['view']:
            animals = animals.filter(view=form.cleaned_data['view'])
        if form.cleaned_data['place']:
            animals = animals.filter(place=form.cleaned_data['place']).distinct()
        if form.cleaned_data['food']:
            animals = animals.filter(food__food_name__in=form.cleaned_data['food']).distinct()
        if form.cleaned_data['recently']:
            recent_date = timezone.now() - timedelta(days=180)
            animals = animals.filter(receipt_date__gte=recent_date)

    context = {
        'form': form,
        'animals': animals,
        'count': animals.count()
    }

    return render(request, 'superuser/superuser_animals.html', context)


@staff_member_required()
def super_user_places_list(request):
    if not request.user.is_superuser:
        return redirect("zoo:my_animals")

    places = Place.objects.all()
    return render(request, 'superuser/superuser_places.html', {"places": places})


@staff_member_required()
def super_user_place(request, pk):
    if not request.user.is_superuser:
        return redirect("zoo:my_animals")

    item = get_object_or_404(Place, pk=pk)
    return render(request, 'superuser/superuser_place_item.html', {"place": item})


@staff_member_required()
def super_user_employees_list(request):
    if not request.user.is_superuser:
        return redirect("zoo:my_animals")

    employees = Employee.objects.all()
    return render(request, 'superuser/superuser_employees.html', {"employees": employees})


@staff_member_required()
def super_user_employee(it_request, pk):
    if not it_request.user.is_superuser:
        return redirect("zoo:my_animals")

    employee = get_object_or_404(Employee, pk=pk)
    places = Place.objects.all()
    filtered = {}
    for i in places:
        for j in i.animals.all().distinct():
            if j.employee == employee:
                filtered[i] = i
    joke_age = 0
    try:
        a = requests.get(f"https://api.agify.io/?name={employee.name}")
        joke_age = int(a.json()["age"])
    except:
        joke_age = -1

    return render(it_request, 'superuser/superuser_employee_item.html',
                  {"employee": employee, "age": joke_age, 'places': filtered.keys()})


@staff_member_required()
def chart_page(request):
    food_counts = {}
    for food_name in FoodName.objects.all():
        count = Animal.objects.filter(food__food_name=food_name).distinct().count()
        food_counts[food_name.name] = count

    labels = food_counts.keys()
    sizes = food_counts.values()

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, startangle=90)
    ax.axis('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    print(plt)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'superuser/chart_page.html', {'data': uri})
