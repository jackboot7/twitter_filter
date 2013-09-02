from django.conf.urls import *
from apps.filtering.views import *


urlpatterns = patterns('apps.filtering.views',

    url(r'edit/(?P<pk>\w+)', FilteringDetailView.as_view()),    # module main view

    url(r'check_status/(?P<pk>\w+)', CheckStatusView.as_view()),
    url(r'switch_status/(?P<pk>\w+)', SwitchStatusView.as_view()),

    url(r'^timeblock/list/(?P<pk>\w+)', TimeBlockListView.as_view()),
    url(r'^timeblock/add/', TimeBlockCreateView.as_view()),
    url(r'^timeblock/delete/(?P<pk>\w+)', TimeBlockDeleteView.as_view()),
    url(r'^timeblock/update/(?P<pk>\w+)', TimeBlockUpdateView.as_view()),

    url(r'^trigger/list/(?P<pk>\w+)', TriggerListView.as_view()),
    url(r'^trigger/delete/(?P<pk>\w+)', TriggerDeleteView.as_view()),
    url(r'^trigger/add', TriggerCreateView.as_view()),

    url(r'^filter/list/(?P<pk>\w+)', FilterListView.as_view()),
    url(r'^filter/delete/(?P<pk>\w+)', FilterDeleteView.as_view()),
    url(r'^filter/add', FilterCreateView.as_view()),

    url(r'^blocked_user/list/(?P<pk>\w+)', BlockedUserListView.as_view()),
    url(r'^blocked_user/delete/(?P<pk>\w+)', BlockedUserDeleteView.as_view()),
    url(r'^blocked_user/add', BlockedUserCreateView.as_view()),
)