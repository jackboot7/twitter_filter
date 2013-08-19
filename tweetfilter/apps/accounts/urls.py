from django.conf.urls import *
from apps.accounts.views import ChannelListView, DeleteChannelView, ChangeStatusView, ChannelDetailView, \
    TimeBlockListView, TimeBlockCreateView, TimeBlockDeleteView, ScheduledPostsDetailView, TwitterAuthenticationView, AuthCallbackView


urlpatterns = patterns('apps.accounts.views',

    url(r'^authenticate/', TwitterAuthenticationView.as_view()),
    url(r'^auth_callback', AuthCallbackView.as_view()),

    url(r'^list', ChannelListView.as_view()),
    url(r'^delete/(?P<pk>\w+)', DeleteChannelView.as_view()),
    url(r'^changestatus/(?P<pk>\w+)', ChangeStatusView.as_view()),

    url(r'^edit/(?P<pk>\w+)', ChannelDetailView.as_view()),
    url(r'scheduled_posts/(?P<pk>\w+)', ScheduledPostsDetailView.as_view()),

    url(r'^timeblock/list/(?P<pk>\w+)', TimeBlockListView.as_view()),
    url(r'^timeblock/add/', TimeBlockCreateView.as_view()),
    url(r'^timeblock/delete/(?P<pk>\w+)', TimeBlockDeleteView.as_view()),
)