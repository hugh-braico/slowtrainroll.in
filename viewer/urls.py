from django.urls import path

from . import views

app_name = 'viewer'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('backup.csv', views.csv, name='csv')
]