from django.urls import path
from . import views

app_name = 'guides'

urlpatterns = [
    path('guide.html', views.guide, name='guide'),
    #path('emg.html', views.emg, name='emg'),
    path('emgs.html', views.ScenarioQuestionListView.as_view(), name='emgs'),
]
