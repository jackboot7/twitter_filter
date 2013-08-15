from django.conf.urls import *
from apps.filtering.views import TriggerDeleteView, TriggerCreateView, TriggerListView, FilterDeleteView, FilterCreateView, FilterListView, BlockedUserListView, BlockedUserDeleteView, BlockedUserAddView

urlpatterns = patterns('apps.filtering.views',

    url(r'^trigger/list/(?P<pk>\w+)', TriggerListView.as_view()),
    url(r'^trigger/delete/(?P<pk>\w+)', TriggerDeleteView.as_view()),
    url(r'^trigger/add', TriggerCreateView.as_view()),

    url(r'^filter/list/(?P<pk>\w+)', FilterListView.as_view()),
    url(r'^filter/delete/(?P<pk>\w+)', FilterDeleteView.as_view()),
    url(r'^filter/add', FilterCreateView.as_view()),

    url(r'^blocked_user/list/(?P<pk>\w+)', BlockedUserListView.as_view()),
    url(r'^blocked_user/delete/(?P<pk>\w+)', BlockedUserDeleteView.as_view()),
    url(r'^blocked_user/add', BlockedUserAddView.as_view())
)