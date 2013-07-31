from django.conf.urls import *
from apps.channels.views import ChannelListView, DeleteChannelView, ChangeStatusView, ChannelDetailView, TimeblockListView


urlpatterns = patterns('apps.channels.views',

    url(r'^list', ChannelListView.as_view()),
    url(r'^delete/(?P<pk>\w+)', DeleteChannelView.as_view()),
    url(r'^changestatus/(?P<pk>\w+)', ChangeStatusView.as_view()),
    url(r'^edit/(?P<pk>\w+)', ChannelDetailView.as_view()),

    url(r'^timeblock/list/(?P<pk>\w+)', TimeblockListView.as_view())

)