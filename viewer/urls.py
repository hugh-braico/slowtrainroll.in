from django.urls import path

from . import views

app_name = 'viewer'

urlpatterns = [
    path('', views.index, name='index'),
    path('backup.csv', views.csv, name='csv')
]