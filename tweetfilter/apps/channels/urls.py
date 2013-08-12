from django.conf.urls import *
from apps.channels.views import ChannelListView, DeleteChannelView, ChangeStatusView, ChannelDetailView, TimeBlockListView, TimeBlockCreateView, TimeBlockDeleteView


urlpatterns = patterns('apps.channels.views',

    url(r'^authenticate/', 'authenticate'),
    url(r'^auth_callback', 'auth_callback'),

    url(r'^list', ChannelListView.as_view()),
    url(r'^delete/(?P<pk>\w+)', DeleteChannelView.as_view()),
    url(r'^changestatus/(?P<pk>\w+)', ChangeStatusView.as_view()),
    url(r'^edit/(?P<pk>\w+)', ChannelDetailView.as_view()),

    url(r'^timeblock/list/(?P<pk>\w+)', TimeBlockListView.as_view()),
    url(r'^timeblock/add/', TimeBlockCreateView.as_view()),
    url(r'^timeblock/delete/(?P<pk>\w+)', TimeBlockDeleteView.as_view()),
)