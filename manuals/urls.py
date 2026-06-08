from django.urls import path
from . import views

app_name = 'manuals'

urlpatterns = [
    path('manual.html', views.manual, name='manual'),
]
