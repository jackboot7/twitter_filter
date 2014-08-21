# -*- coding: utf-8 -*-

import json
import logging
import datetime

from django.forms.models import model_to_dict
from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin, LoginRequiredMixin
from django.http.response import HttpResponse
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.accounts.models import Channel, ItemGroup
from apps.scheduling.models import ScheduledTweet
from apps.twitter.api import ChannelAPI


logger = logging.getLogger('app')


class ScheduledPostsHomeView(LoginRequiredMixin, ListView):
    """
    Renders the main interface for scheduling module config
    """
    template_name = "scheduling/settings.html"
    queryset = ItemGroup.objects.filter(channel_exclusive=False)

    def get_context_data(self, **kwargs):
        context = super(ScheduledPostsHomeView, self).get_context_data(**kwargs)
        context['scheduled_tweet_groups'] = self.get_queryset().filter(content_type="ScheduledTweet")
        context['channel_list'] = Channel.objects.filter(user_id=self.request.user.id)
        return context


class SchedulingDetailView(LoginRequiredMixin, DetailView):
    """
    Renders the interface for scheduling settings from a particular channel
    """
    model = Channel
    template_name = "scheduling/channel_index.html"
    context_object_name = "channel"

    def get_context_data(self, **kwargs):
        groups_queryset = ItemGroup.objects.filter(channel_exclusive=False)
        context = super(SchedulingDetailView, self).get_context_data(**kwargs)
        context['scheduled_tweet_groups'] = groups_queryset.filter(content_type="ScheduledTweet")

        return context


#==========================
# Scheduling Config
#==========================
class CheckStatusView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    """
    Returns scheduling module status (is it enabled or disabled?)
    """
    model = Channel

    def get_ajax(self, request,  *args, **kwargs):
        obj = self.get_object()

        if obj.scheduling_enabled:
            response_data = {'result': "enabled"}
        else:
            response_data = {'result': "disabled"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchStatusView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Enables or disables automatic retweets
    """
    model = Channel

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            if obj.scheduling_enabled:
                # disable
                scheduled_tweets = ScheduledTweet.objects.filter(channel=obj.screen_name)
                for tweet in scheduled_tweets:
                    if tweet.status == ScheduledTweet.STATUS_ENABLED:
                        pt = tweet.periodic_task
                        pt.enabled = False
                        pt.save()
                obj.scheduling_enabled = False
                obj.save()
            else:
                # enable
                scheduled_tweets = ScheduledTweet.objects.filter(channel=obj.screen_name)
                for tweet in scheduled_tweets:
                    if tweet.status == ScheduledTweet.STATUS_ENABLED:
                        pt = tweet.periodic_task
                        pt.enabled = True
                        pt.save()
                obj.scheduling_enabled = True
                obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in SwitchStatusView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ScheduledTweetListView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DetailView):
    model = ItemGroup
    context_object_name = "scheduled_tweet_list"

    def get_ajax(self, request, *args, **kwargs):
        objs = ScheduledTweet.objects.filter(group=self.get_object())
        json_list = []

        for scheduled_tweet in objs:
            dias = ""
            if scheduled_tweet.monday:
                dias = "Lun "
            if scheduled_tweet.tuesday:
                dias += "Mar "
            if scheduled_tweet.wednesday:
                dias += "Mie "
            if scheduled_tweet.thursday:
                dias += "Jue "
            if scheduled_tweet.friday:
                dias += "Vie "
            if scheduled_tweet.saturday:
                dias += "Sab "
            if scheduled_tweet.sunday:
                dias += "Dom "
            if len(dias) == 28:
                dias = u"Todos los días"

            json_list.append({
                'id': scheduled_tweet.id,
                'text': scheduled_tweet.text,
                'text_excerpt': scheduled_tweet.get_excerpt(),
                'date_time': ("%s (%s)") % (scheduled_tweet.time.strftime("%H:%M"), dias),
                'time': scheduled_tweet.time.strftime("%H:%M"),
                'monday': scheduled_tweet.monday,
                'tuesday': scheduled_tweet.tuesday,
                'wednesday': scheduled_tweet.wednesday,
                'thursday': scheduled_tweet.thursday,
                'friday': scheduled_tweet.friday,
                'saturday': scheduled_tweet.saturday,
                'sunday': scheduled_tweet.sunday,
            })

        return self.render_json_response(json_list)


class ScheduledTweetCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = ScheduledTweet

    def post_ajax(self, request, *args, **kwargs):

        try:
            group = ItemGroup.objects.filter(id=request.POST['group_id'])[0]
            
            block = ScheduledTweet()
            block.text = request.POST['text']
            block.time = datetime.datetime.strptime(request.POST['time'], "%H:%M").time()
            block.monday = True if request.POST['monday'] == "1" else False
            block.tuesday = True if request.POST['tuesday'] == "1" else False
            block.wednesday = True if request.POST['wednesday'] == "1" else False
            block.thursday = True if request.POST['thursday'] == "1" else False
            block.friday = True if request.POST['friday'] == "1" else False
            block.saturday = True if request.POST['saturday'] == "1" else False
            block.sunday = True if request.POST['sunday'] == "1" else False
            block.group = group
            block.save()
            response_data = {'result': "ok"}
        except Exception, e:
            logger.exception("Error while creating scheduled tweet")
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ScheduledTweetSendView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):

    def post_ajax(self, request, *args, **kwargs):
        tweet_id = kwargs['pk']
        tweet_obj = ScheduledTweet.objects.filter(id=tweet_id)[0]
        group = tweet_obj.group
        for channel in group.channel_set.all():
            api = ChannelAPI(channel)
            try:
                api.tweet(tweet_obj.text)
                response_data = {'result': "ok"}
            except Exception, e:
                """
                if "duplicate" in e.args[0]:
                    msg = u"Este mensaje ya se ha enviado recientemente"
                elif "update limit" in e.args[0]:
                    msg = u"El canal no puede publicar por razones de 'update limit'"
                elif "unauthorized" in e.args[0]:
                    msg = u"La cuenta actual no está autorizada para publicar. " \
                          u"Se recomienda revocar la aplicación desde twitter y volver a registrar el canal"
                else:
                    msg = args[0]
                    response_data = {'result': "fail", 'error_msg': msg}
                """
                # acumular mensajes de error
                pass

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ScheduledTweetDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = ScheduledTweet
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ScheduledTweetUpdateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    model = ScheduledTweet

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.text = request.POST['text']
            obj.time = datetime.datetime.strptime(request.POST['time'], "%H:%M").time()
            obj.monday = True if request.POST['monday'] == "1" else False
            obj.tuesday = True if request.POST['tuesday'] == "1" else False
            obj.wednesday = True if request.POST['wednesday'] == "1" else False
            obj.thursday = True if request.POST['thursday'] == "1" else False
            obj.friday = True if request.POST['friday'] == "1" else False
            obj.saturday = True if request.POST['saturday'] == "1" else False
            obj.sunday = True if request.POST['sunday'] == "1" else False
            obj.save()
            response_data = {'result': "ok"}
        except Exception, e:
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


#==============
# Groups views
#==============

class ScheduledTweetGroupCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    """
    Creates a new ScheduledTweet group
    """
    model = ItemGroup

    def post_ajax(self, request, *args, **kwargs):
        try:
            scheduled_tweet_groups = ItemGroup.objects.filter(content_type="ScheduledTweet")
            for group in scheduled_tweet_groups:
                if group.name == request.POST['scheduled_tweet_group_name']:
                    response_data = {'result': "duplicate"}
                    break
            else:
                new_group = ItemGroup()
                new_group.content_type = "ScheduledTweet"
                new_group.name = request.POST['scheduled_tweet_group_name']
                new_group.save()
                response_data = {'result': "ok", 'group_obj': model_to_dict(new_group)}
        except Exception, e:
            logger.exception("Error al crear grupo de ScheduledTweet")
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ScheduledTweetGroupUpdateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Update ScheduledTweet group attributes
    """
    model = ItemGroup

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            scheduled_tweet_groups = ItemGroup.objects.filter(content_type="ScheduledTweet").exclude(id=obj.id)
            for group in scheduled_tweet_groups:
                if group.name == request.POST['scheduled_tweet_group_name']:
                    response_data = {'result': "duplicate"}
                    break
            else:
                obj.name = request.POST['scheduled_tweet_group_name']
                obj.save()
                response_data = {'result': "ok"}
        except Exception, e:
            response_data = {'result': e.args[0]}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ScheduledTweetGroupListView(JSONResponseMixin, AjaxResponseMixin, ListView):
    """
    Shows a all non-exclusive scheduled tweet groups
    """
    queryset = ItemGroup.objects.filter(content_type="ScheduledTweet").filter(channel_exclusive=False)

    def get_ajax(self, request, *args, **kwargs):
        json_list = []
        group_list = self.get_queryset()

        for group in group_list:
            group_dict = model_to_dict(group)
            group_dict['channels'] = []
            
            for chan in group.channel_set.all():
                group_dict['channels'].append(chan.screen_name)
            
            json_list.append(group_dict)

        return self.render_json_response(json_list)


class ScheduledTweetGroupListChannelView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    """
    Shows a all scheduled tweet groups linked to a particular channel
    """
    model = Channel

    def get_ajax(self, request, *args, **kwargs):
        json_list = []
        group_list = self.get_object().groups.filter(content_type="ScheduledTweet")

        for group in group_list:
            group_dict = model_to_dict(group)
            json_list.append(group_dict)

        return self.render_json_response(json_list)


class SetItemGroupChannelsView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Associates a list of channels to the item group
    """
    model = ItemGroup

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            channels = json.loads(request.POST['channels'])
            obj.channel_set.clear()
            
            for chan in channels:
                obj.channel_set.add(chan)

            obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in SwitchStatusView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ItemGroupChannelListView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    """
    Given an item group, returns all channels associated with it
    """
    model = ItemGroup

    def get_ajax(self, request,  *args, **kwargs):
        obj = self.get_object()
        response_data = []
        
        for chan in obj.channel_set.all():
            response_data.append(chan.screen_name)

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ItemGroupDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    """
    Deletes an item group
    """
    model = ItemGroup
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ChannelUnlinkGroupView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Removes the association between a channel and an ItemGroup
    """
    model = Channel

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.groups.remove(request.POST['group_id'])
            
            obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in ChannelUnlinkGroupView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SetChannelGroupsView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Associates a list of groups to the channel
    """
    model = Channel

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            linked_groups = obj.groups.filter(content_type=request.POST['content_type']).exclude(channel_exclusive=True)
            new_groups = json.loads(request.POST['groups'])

            obj.groups.remove(*linked_groups)
            
            if new_groups:
                obj.groups.add(*new_groups)
            
            obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in SetChannelGroupsView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ListChannelGroupsView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    """
    Given an item group, returns all channels associated with it
    """
    model = Channel

    def get_ajax(self, request,  *args, **kwargs):
        obj = self.get_object()
        response_data = []
        
        for group in obj.groups.filter(content_type=request.GET['content_type']):
            response_data.append(group.id)

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")

