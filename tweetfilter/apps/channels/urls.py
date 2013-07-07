from django.conf.urls import *
from apps.channels.views import ChannelListView, DeleteChannelView, ChangeStatusView


urlpatterns = patterns('apps.channels.views',

    url(r'^list', ChannelListView.as_view()),
    url(r'^delete/(?P<pk>\w+)', DeleteChannelView.as_view()),
    url(r'^changestatus/(?P<pk>\w+)', ChangeStatusView.as_view())

)