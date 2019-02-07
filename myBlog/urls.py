"""myBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin', include(admin.site.urls)),
    url(r'^favicon.ico$',RedirectView.as_view(url=r'static/favicon.ico')),
    url(r'^user/',include('user.urls',namespace='user')),#用户模块
    url(r'^content/',include('content.urls',namespace='content')),#页面模块
    url(r'^articleOpt/',include('articleOpt.urls',namespace='articleOpt')),#文章模块
    url(r'^ueditor/', include('DjangoUeditor.urls')), # 百度 ueditor 的路由
    url(r'^',include('content.urls',namespace='con_index')),


]

