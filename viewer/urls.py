from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'viewer'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('backup.csv', views.csv, name='csv'),
    path('old_twb_dump.csv', TemplateView.as_view(template_name='viewer/old_twb_dump.csv', content_type='text/plain'))
]