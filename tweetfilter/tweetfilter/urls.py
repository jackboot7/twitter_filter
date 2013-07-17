from django.conf.urls import patterns, include, url
from django.contrib import admin
from tweetfilter.views import ChannelAddedView
from views import HomeView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^success$', ChannelAddedView.as_view(), name="channel_added"),
    url(r'^test$', 'tweetfilter.views.test'),
    url(r'^auth/', include('apps.auth.urls')),
    url(r'^channels/', include('apps.channels.urls')),
    url(r'^tasks/', include('djcelery.urls')),
    # url(r'^tweetfilter/', include('tweetfilter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
