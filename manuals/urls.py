from django.urls import path
from . import views

app_name = 'manuals'

urlpatterns = [
    path('manual.html', views.manual, name='manual'),
    path('learns.html', views.ManualDetailListView.as_view(), name='learns'),
]
