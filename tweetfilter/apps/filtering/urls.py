# -*- coding: utf-8 -*-

from django.conf.urls import *
from apps.filtering.views import *


urlpatterns = patterns('apps.filtering.views',

    url(r'^$', FilteringHomeView.as_view(), name='filtering_home'),    # module main view
    url(r'edit/(?P<pk>\w+)', FilteringDetailView.as_view(), name='edit_channel'),

    url(r'check_status/(?P<pk>\w+)', CheckStatusView.as_view()),
    url(r'switch_status/(?P<pk>\w+)', SwitchStatusView.as_view()),

    url(r'switch_scheduledblocks/(?P<pk>\w+)', SwitchScheduleBlocksView.as_view()),
    url(r'switch_blacklist/(?P<pk>\w+)', SwitchBlackListView.as_view()),
    url(r'switch_triggers/(?P<pk>\w+)', SwitchTriggersView.as_view()),
    url(r'switch_replacements/(?P<pk>\w+)', SwitchReplacementsView.as_view()),
    url(r'switch_filters/(?P<pk>\w+)', SwitchFiltersView.as_view()),
    url(r'switch_update_limit/(?P<pk>\w+)', SwitchUpdateLimitView.as_view()),

    url(r'^timeblock/list/(?P<pk>\w+)', TimeBlockListView.as_view()),
    url(r'^timeblock/add/', TimeBlockCreateView.as_view()),
    url(r'^timeblock/delete/(?P<pk>\w+)', TimeBlockDeleteView.as_view()),
    url(r'^timeblock/update/(?P<pk>\w+)', TimeBlockUpdateView.as_view()),

    url(r'^trigger/list/(?P<pk>\w+)', TriggerListView.as_view()),
    url(r'^trigger/delete/(?P<pk>\w+)', TriggerDeleteView.as_view()),
    url(r'^trigger/add', TriggerCreateView.as_view()),
    url(r'^trigger/switch_dm/(?P<pk>\w+)', SwitchTriggerDMView.as_view()),
    url(r'^trigger/switch_mention/(?P<pk>\w+)', SwitchTriggerMentionView.as_view()),

    url(r'^replacement/list/(?P<pk>\w+)', ReplacementListView.as_view()),
    url(r'^replacement/delete/(?P<pk>\w+)', ReplacementDeleteView.as_view()),
    url(r'^replacement/add', ReplacementCreateView.as_view()),
    url(r'^replacement/switch_dm/(?P<pk>\w+)', SwitchReplacementDMView.as_view()),
    url(r'^replacement/switch_mention/(?P<pk>\w+)', SwitchReplacementMentionView.as_view()),

    url(r'^filter/list/(?P<pk>\w+)', FilterListView.as_view()),
    url(r'^filter/delete/(?P<pk>\w+)', FilterDeleteView.as_view()),
    url(r'^filter/add', FilterCreateView.as_view()),
    url(r'^filter/switch_dm/(?P<pk>\w+)', SwitchFilterDMView.as_view()),
    url(r'^filter/switch_mention/(?P<pk>\w+)', SwitchFilterMentionView.as_view()),

    url(r'^blocked_user/list/(?P<pk>\w+)', BlockedUserListView.as_view()),
    url(r'^blocked_user/delete/(?P<pk>\w+)', BlockedUserDeleteView.as_view()),
    url(r'^blocked_user/add', BlockedUserCreateView.as_view()),
)
