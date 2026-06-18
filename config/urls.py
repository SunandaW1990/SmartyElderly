"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from index_photo import views as index_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_views.index, name='index'), 
    path('index.html', index_views.index, name='index'), 
    path('accounts/', include('accounts.urls')),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('welcome/', TemplateView.as_view(template_name='welcome.html'), name='welcome'),
    path('manuals/', include('manuals.urls', namespace='manuals')),
    path('stories/', include('stories.urls', namespace='stories')),
    path('courses/', include('courses.urls', namespace='courses')),
    path('antiscamtools/', include('antiscamtools.urls', namespace='antiscamtools')),
    path('guides/', include('guides.urls', namespace='guides')),
    path('subscribes/', include('subscribes.urls', namespace='subscribes')),
    # 純靜態頁面（無需資料庫）
    path('abouts/', TemplateView.as_view(template_name='abouts.html'), name='abouts'),
    path('abouts.html', TemplateView.as_view(template_name='abouts.html'), name='abouts.html'),
    path('games/', TemplateView.as_view(template_name='games.html'), name='games'),
    path('games.html', TemplateView.as_view(template_name='games.html'), name='games.html'),
    path('helps/', TemplateView.as_view(template_name='helps.html'), name='helps'),
    path('helps.html', TemplateView.as_view(template_name='helps.html'), name='helps.html'),    
    path('news/', TemplateView.as_view(template_name='news.html'), name='news'),
    path('news.html', TemplateView.as_view(template_name='news.html'), name='news.html'),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()

admin.site.site_header = 'SmartyElderly Administration'
admin.site.site_title = 'SmartyElderly Admin Portal'
admin.site.index_title = 'Welcome to SmartyElderly Admin Portal'