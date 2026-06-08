from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('course.html', views.course, name='course'),
]
