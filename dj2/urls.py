#coding:utf-8
"""
dj2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from main import front_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 前台页面
    path('', front_views.index_view, name='index'),
    
    # API接口
    path('api/products', front_views.api_products),
    path('api/recommend', front_views.api_recommend),
    path('api/forums', front_views.api_forums),
    path('api/news', front_views.api_news),
    path('api/stats', front_views.api_stats),
    path('api/record_behavior', front_views.api_record_behavior),
    
    # 安全相关接口
    path('security/', include('main.urls')),
    
    # 主应用路由
    path('main/', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
