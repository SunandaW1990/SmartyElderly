from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('story.html', views.story, name='story'),
]
