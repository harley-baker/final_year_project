from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyse/<string:url>', views.analyse, name='analyse')
]
