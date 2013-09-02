from django.conf.urls import *
from apps.scheduling.views import *


urlpatterns = patterns('apps.scheduling.views',

    url(r'^edit/(?P<pk>\w+)', ScheduledPostsDetailView.as_view()),   # module main view

    url(r'check_status/(?P<pk>\w+)', CheckStatusView.as_view()),
    url(r'switch_status/(?P<pk>\w+)', SwitchStatusView.as_view()),

    url(r'^list/(?P<pk>\w+)', ScheduledTweetListView.as_view()),
    url(r'^add', ScheduledTweetCreateView.as_view()),
    url(r'^delete/(?P<pk>\w+)', ScheduledTweetDeleteView.as_view()),
    url(r'^update/(?P<pk>\w+)', ScheduledTweetUpdateView.as_view())

)