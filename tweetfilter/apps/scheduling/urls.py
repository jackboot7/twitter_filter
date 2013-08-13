from django.conf.urls import *
from apps.scheduling.views import ScheduledTweetkListView, ScheduledTweetCreateView, ScheduledTweetDeleteView, ScheduledTweetkEditView


urlpatterns = patterns('apps.scheduling.views',


    url(r'^list/(?P<pk>\w+)', ScheduledTweetkListView.as_view()),
    url(r'^add', ScheduledTweetCreateView.as_view()),
    url(r'^delete', ScheduledTweetDeleteView.as_view()),
    #url(r'^changestatus/(?P<pk>\w+)', ),
    url(r'^edit', ScheduledTweetkEditView.as_view()),

)