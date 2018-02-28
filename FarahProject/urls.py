"""FarahProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from collection import views
from os import path

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^start-session', views.start, name='start'),
    url(r'^select-participant', views.select, name='select'),
    url(r'^select-assessment-session', views.select_type, name='select-type'),
    url(r'^selection-redirect', views.selection_redirect, name='selection-redirect'),
    url(r'^paired-report', views.report_paired_results, name='paired-report'),
    url(r'^conjugate-report', views.report_conjugate_results, name='conjugate-report'),
    url(r'^download_results/(?P<user_id>[a-zA-Z0-9]+)/', views.download_results, name='download-results'),
    url(r'^end-sesssion', views.end_session, name='end-session'),
    url(r'^$', views.index, name='index'),
]

urlpatterns += [
    url(r'accounts/', include('django.contrib.auth.urls')),
]
