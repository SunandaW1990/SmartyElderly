from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('courses.html', views.courses, name='courses'),
    path('courses', views.enroll, name='enroll'),
#    path('courses/<str:result>/<str:course_id>', views.enrollresult, name='enrollresult'),
    path('course.html', views.course, name='course'),
]
