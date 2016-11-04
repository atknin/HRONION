# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import include, url, patterns
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
import CRDB.urls
from CRDB.views import (chem_list, chem_detail, index, 
    converter, article_list, try_l, add_comment, 
    article_detail, file_converter_def, converter_detail, 
    add_suggest, forbidden, references, like, profile, 
    double_crystal, theory, add_paper,scedule)


urlpatterns = [
    url(r'^startup/', include('HRONION.urls')),
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),
    url(r'^chem_list/', chem_list, name = 'chem_list'),
    url(r'^like/$', like, name='like'),
    url(r'^file_upload_converter/(?P<project_id>\d+)/', file_converter_def, name = 'file_converter_def'), 
    url(r'^converter_detail/(?P<file_id>\d+)/', converter_detail, name = 'converter_detail'),
    url(r'^chem_detail/(?P<periodic_table_number>\d+)/', chem_detail, name = 'chem_detail'),
    url(r'^article_detail/(?P<satya_id>\d+)/', article_detail, name = 'article_detail'),
    url(r'^add_comment/(?P<project_id>\d+)/', add_comment, name = 'add_comment'),
    url(r'^add_paper/', add_paper, name = 'add_paper'),
    url(r'^scedule/', scedule, name = 'scedule'),
    url(r'^add_suggest/(?P<project_id>\d+)/', add_suggest, name = 'add_suggest'), 
    url(r'^converter/', converter, name = 'converter'),
    url(r'^theory/', theory, name = 'theory'),
    url(r'^forbidden/', forbidden, name = 'forbidden'),
    url(r'^double_crystal/', double_crystal, name = 'double_crystal'),
    url(r'^references/', references, name = 'references'),
    url(r'^accounts/profile/', profile, name ='profile'),
    url(r'^article_list/', article_list, name = 'article_list'),
    url(r'^donot/', try_l, name = 'try_l'),
    url(r'^', index, name ='index'),  

] 

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]
    
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

