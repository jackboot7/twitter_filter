from django.conf.urls import *
from apps.scheduling.views import ScheduledTweetListView, ScheduledTweetCreateView, ScheduledTweetDeleteView, ScheduledPostsDetailView


urlpatterns = patterns('apps.scheduling.views',

    url(r'^edit/(?P<pk>\w+)', ScheduledPostsDetailView.as_view()),   # module main view

    url(r'^list/(?P<pk>\w+)', ScheduledTweetListView.as_view()),
    url(r'^add', ScheduledTweetCreateView.as_view()),
    url(r'^delete/(?P<pk>\w+)', ScheduledTweetDeleteView.as_view()),

)