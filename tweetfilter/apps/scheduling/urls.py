from django.conf.urls import *
from apps.scheduling.views import *


urlpatterns = patterns('apps.scheduling.views',

    url(r'^$', ScheduledPostsHomeView.as_view(), name="scheduling_home"),
    url(r'^edit/(?P<pk>\w+)', SchedulingDetailView.as_view()),

    url(r'check_status/(?P<pk>\w+)', CheckStatusView.as_view()),
    url(r'switch_status/(?P<pk>\w+)', SwitchStatusView.as_view()),

    url(r'^scheduled_tweet_group/add/', ScheduledTweetGroupCreateView.as_view()),
    url(r'^scheduled_tweet_group/update/(?P<pk>\w+)', ScheduledTweetGroupUpdateView.as_view(), name="edit_scheduled_tweet_group"),
    url(r'^scheduled_tweet_group/list/', ScheduledTweetGroupListView.as_view()),
    url(r'^scheduled_tweet_group/channel/(?P<pk>\w+)', ScheduledTweetGroupListChannelView.as_view()),
    url(r'^scheduled_tweet_group/delete/(?P<pk>\w+)', ItemGroupDeleteView.as_view()),
    url(r'^scheduled_tweet_group/set_channels/(?P<pk>\w+)', SetItemGroupChannelsView.as_view()),
    url(r'^scheduled_tweet_group/list_channels/(?P<pk>\w+)', ItemGroupChannelListView.as_view()),


    url(r'^scheduled_tweet/list/(?P<pk>\w+)', ScheduledTweetListView.as_view()),
    url(r'^scheduled_tweet/add', ScheduledTweetCreateView.as_view()),
    url(r'^scheduled_tweet/send/(?P<pk>\w+)', ScheduledTweetSendView.as_view()),
    url(r'^scheduled_tweet/delete/(?P<pk>\w+)', ScheduledTweetDeleteView.as_view()),
    url(r'^scheduled_tweet/update/(?P<pk>\w+)', ScheduledTweetUpdateView.as_view()),

    url(r'^channel/set_groups/(?P<pk>\w+)', SetChannelGroupsView.as_view()),
    url(r'^channel/list_groups/(?P<pk>\w+)', ListChannelGroupsView.as_view()),
    url(r'^channel/unlink_group/(?P<pk>\w+)', ChannelUnlinkGroupView.as_view()),
)