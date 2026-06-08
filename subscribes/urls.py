from django.urls import path
from . import views

app_name = 'subscribes'

urlpatterns = [
    path('subscribe.html', views.subscribe, name='subscribe'),
]
