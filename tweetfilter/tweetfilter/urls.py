from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import HomeView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^success$', HomeView.as_view(channel_added="true"), name='channel_added'),
    url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^tasks/', include('djcelery.urls')),
    url(r'^filtering/', include('apps.filtering.urls')),
    url(r'^scheduling/', include('apps.scheduling.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
