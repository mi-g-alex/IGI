from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from . import views

app_name = "zoo"

urlpatterns = [
    path('', views.index, name='home_page'),
    re_path(r'^about/?$', views.about, name='about_page'),
    re_path(r'^news/?$', views.news, name='news_page'),
    path('news/<int:pk>', views.news_detail, name='news_detail'),
    re_path(r'^terms/?$', views.terms, name='terms_page'),
    re_path(r'^vacancy/?$', views.vacancy, name='vacancy_page'),
    re_path(r'^policy/?$', views.policy, name='policy_page'),
    re_path(r'^promo/?$', views.promo, name='promo_page'),
    re_path(r'^reviews/?$', views.reviews, name='reviews_page'),
    re_path(r'^animals/?$', views.animal_list, name='animal_list'),

    re_path(r'^registration/?$', views.register, name='auth_registration'),
    re_path(r'^login/?$', views.Login.as_view(), name='auth_login'),
    re_path(r'^logout/?$', views.my_logout, name='auth_logout'),

    re_path(r'^profile/?$', views.profile, name='profile'),
    re_path(r'^create_review/?$', views.create_comment, name='new_review'),
    re_path(r'^buy_ticket/?$', views.buy_ticket, name='buy_ticket'),
    re_path(r'^my_tickets/?$', views.my_tickets, name='my_tickets'),

    re_path(r'^my_animals/?$', views.my_animals, name='my_animals'),
    path('animals/<int:pk>', views.animal_detail, name='my_animal_detail'),

    re_path(r'^super/all_animals/?$', views.super_user_animal_list, name='superuser_all_animals'),
    re_path(r'^super/all_places/?$', views.super_user_places_list, name='superuser_all_places'),
    path('super/places/<int:pk>', views.super_user_place, name='superuser_place_details'),
    re_path(r'^super/employees/?$', views.super_user_employees_list, name='superuser_all_employees'),
    path('super/employees/<int:pk>', views.super_user_employee, name='superuser_employee_details'),
    path('super/chart', views.chart_page, name='superuser_chart'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)