# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribe.html', views.subscribe, name='subscribe.html'),
    # 儀表板相關路由（需要登入）
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard.html', views.dashboard, name='dashboard.html'),
    path('dashboard/update-notification/', views.update_notification, name='update_notification'),
    path('dashboard/update-profile/', views.update_profile, name='update_profile'),
    path('dashboard/update-courses/', views.update_courses, name='update_courses'),
    path('dashboard/send-message/', views.send_message, name='send_message'),
]