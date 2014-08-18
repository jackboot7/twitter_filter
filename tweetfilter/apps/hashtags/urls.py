from django.conf.urls import *

from apps.hashtags.views import *


urlpatterns = patterns('apps.hashtags.views',

    url(r'^hashtag_group/add/', HashtagGroupCreateView.as_view()),
    url(r'^hashtag_group/update/(?P<pk>\w+)', HashtagGroupUpdateView.as_view(), name="edit_hashtag_group"),
    url(r'^hashtag_group/list/', HashtagGroupListView.as_view()),
    url(r'^hashtag_group/delete/(?P<pk>\w+)', ItemGroupDeleteView.as_view()),
    url(r'^hashtag_group/set_channels/(?P<pk>\w+)', SetItemGroupChannelsView.as_view()),
    url(r'^hashtag_group/list_channels/(?P<pk>\w+)', ItemGroupChannelListView.as_view()),

    url(r'^$', HashtagsHomeView.as_view(), name="hashtags_home"),
    url(r'^edit/(?P<pk>\w+)', HashtagsDetailView.as_view()),

    url(r'check_status/(?P<pk>\w+)', CheckStatusView.as_view()),
    url(r'switch_status/(?P<pk>\w+)', SwitchStatusView.as_view()),

    url(r'^hashtag/list/(?P<pk>\w+)', HashtagListView.as_view()),
    url(r'^hashtag/add', HashtagCreateView.as_view()),
    url(r'^hashtag/update/(?P<pk>\w+)', HashtagUpdateView.as_view()),
    url(r'^hashtag/delete/(?P<pk>\w+)', HashtagDeleteView.as_view()),
    url(r'^hashtag/reset/(?P<pk>\w+)', HashtagResetView.as_view())
)