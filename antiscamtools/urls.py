from django.urls import path
from . import views

app_name = 'antiscamtools'

urlpatterns = [
    path('antiscamtool.html', views.antiscamtool, name='antiscamtool'),
]
