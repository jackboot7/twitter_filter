# -*- coding:utf8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.cache import cache_page
from views import HomeView

from apps.accounts.forms import LoginForm

admin.autodiscover()

"""
HomeView uses cache_page decorator to cache results for 15 minutes
"""

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="home"),
#    url(r'^$', cache_page(60 * 15)(HomeView.as_view()), name="home"),
    url(r'^success$', HomeView.as_view(channel_added="true"), name='channel_added'),
    url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^tasks/', include('djcelery.urls')),
    url(r'^filtering/', include('apps.filtering.urls')),
    url(r'^scheduling/', include('apps.scheduling.urls')),
    url(r'^hashtags/', include('apps.hashtags.urls')),

    url(r'^login/',
        'django.contrib.auth.views.login',
        {'authentication_form': LoginForm},
        name='login'),

    url(r'logout/',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'),


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
