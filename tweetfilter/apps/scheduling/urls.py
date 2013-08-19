from django.conf.urls import *
from apps.scheduling.views import ScheduledTweetListView, ScheduledTweetCreateView, ScheduledTweetDeleteView


urlpatterns = patterns('apps.scheduling.views',

    url(r'^list/(?P<pk>\w+)', ScheduledTweetListView.as_view()),
    url(r'^add', ScheduledTweetCreateView.as_view()),
    url(r'^delete/(?P<pk>\w+)', ScheduledTweetDeleteView.as_view()),
    #url(r'^edit', ScheduledTweetkEditView.as_view()),
)