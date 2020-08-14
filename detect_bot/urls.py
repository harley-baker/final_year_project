from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyse', views.analyse, name='analyse'),
    path('analyse_json', views.analyse_json, name='analyse_json')
]
