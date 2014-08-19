# -*- coding: utf-8 -*-

from django.conf.urls import *
from apps.filtering.views import *


urlpatterns = patterns('apps.filtering.views',

    url(r'edit/(?P<pk>\w+)', FilteringDetailView.as_view(), name='edit_channel'),
    url(r'^$', TriggersHomeView.as_view()), # Main module settings

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

    ##################
    url(r'^trigger_group/$', TriggersHomeView.as_view(), name='triggers_home'),    # module main view
    url(r'^trigger_group/add/', TriggerGroupCreateView.as_view()),
    url(r'^trigger_group/update/(?P<pk>\w+)', TriggerGroupUpdateView.as_view(), name="edit_trigger_group"),
    url(r'^trigger_group/list/', TriggerGroupListView.as_view()),
    url(r'^trigger_group/channel/(?P<pk>\w+)', TriggerGroupListChannelView.as_view()),
    url(r'^trigger_group/delete/(?P<pk>\w+)', ItemGroupDeleteView.as_view()),
    url(r'^trigger_group/set_channels/(?P<pk>\w+)', SetItemGroupChannelsView.as_view()),
    url(r'^trigger_group/list_channels/(?P<pk>\w+)', ItemGroupChannelListView.as_view()),
    
    url(r'^replacement_group/$', ReplacementsHomeView.as_view(), name='replacements_home'),
    url(r'^replacement_group/add/', ReplacementGroupCreateView.as_view()),
    url(r'^replacement_group/update/(?P<pk>\w+)', ReplacementGroupUpdateView.as_view(), name="edit_replacement_group"),
    url(r'^replacement_group/list/', ReplacementGroupListView.as_view()),
    url(r'^replacement_group/delete/(?P<pk>\w+)', ItemGroupDeleteView.as_view()),
    url(r'^replacement_group/set_channels/(?P<pk>\w+)', SetItemGroupChannelsView.as_view()),
    url(r'^replacement_group/list_channels/(?P<pk>\w+)', ItemGroupChannelListView.as_view()),

    url(r'^filter_group/$', FiltersHomeView.as_view(), name='filters_home'),
    url(r'^filter_group/add/', FilterGroupCreateView.as_view()),
    url(r'^filter_group/update/(?P<pk>\w+)', FilterGroupUpdateView.as_view(), name="edit_filter_group"),
    url(r'^filter_group/list/', FilterGroupListView.as_view()),
    url(r'^filter_group/delete/(?P<pk>\w+)', ItemGroupDeleteView.as_view()),
    url(r'^filter_group/set_channels/(?P<pk>\w+)', SetItemGroupChannelsView.as_view()),
    url(r'^filter_group/list_channels/(?P<pk>\w+)', ItemGroupChannelListView.as_view()),

    url(r'^blocked_user_group/$', BlockedUsersHomeView.as_view(), name='blocked_users_home'),
    url(r'^blocked_user_group/add/', BlockedUserGroupCreateView.as_view()),
    url(r'^blocked_user_group/update/(?P<pk>\w+)', BlockedUserGroupUpdateView.as_view(), name="edit_blocked_user_group"),
    url(r'^blocked_user_group/list/', BlockedUserGroupListView.as_view()),
    url(r'^blocked_user_group/delete/(?P<pk>\w+)', ItemGroupDeleteView.as_view()),
    url(r'^blocked_user_group/set_channels/(?P<pk>\w+)', SetItemGroupChannelsView.as_view()),
    url(r'^blocked_user_group/list_channels/(?P<pk>\w+)', ItemGroupChannelListView.as_view()),
)
