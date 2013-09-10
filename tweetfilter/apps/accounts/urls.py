from django.conf.urls import *
from apps.accounts.views import ChannelListView, DeleteChannelView, TwitterAuthenticationView, AuthCallbackView


urlpatterns = patterns('apps.accounts.views',

    url(r'^authenticate/', TwitterAuthenticationView.as_view()),
    url(r'^auth_callback', AuthCallbackView.as_view()),

    url(r'^list', ChannelListView.as_view()),
    url(r'^delete/(?P<pk>\w+)', DeleteChannelView.as_view()),
)