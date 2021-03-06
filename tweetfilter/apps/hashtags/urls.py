from django.conf.urls import *

from apps.hashtags.views import *


urlpatterns = patterns('apps.hashtags.views',

    url(r'^edit/(?P<pk>\w+)', HashtagsDetailView.as_view()),   # module main view

    url(r'check_status/(?P<pk>\w+)', CheckStatusView.as_view()),
    url(r'switch_status/(?P<pk>\w+)', SwitchStatusView.as_view()),

    url(r'^list/(?P<pk>\w+)', HashtagListView.as_view()),
    url(r'^add', HashtagCreateView.as_view()),
    url(r'^update/(?P<pk>\w+)', HashtagUpdateView.as_view()),
    url(r'^delete/(?P<pk>\w+)', HashtagDeleteView.as_view()),
    url(r'^reset/(?P<pk>\w+)', HashtagResetView.as_view())
)