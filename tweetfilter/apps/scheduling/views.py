# -*- coding: utf-8 -*-

import json
import logging
from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin
import datetime
from django.http.response import HttpResponse
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView
from apps.accounts.models import Channel
from apps.scheduling.models import ScheduledTweet

logger = logging.getLogger('app')

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

        if obj.schedulingconfig.scheduling_enabled:
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
            if obj.schedulingconfig.scheduling_enabled:
                # disable
                scheduled_tweets = ScheduledTweet.objects.filter(channel=obj.screen_name)
                for tweet in scheduled_tweets:
                    if tweet.status == ScheduledTweet.STATUS_ENABLED:
                        pt = tweet.periodic_task
                        pt.enabled = False
                        pt.save()
                obj.schedulingconfig.scheduling_enabled = False
                obj.schedulingconfig.save()
            else:
                # enable
                scheduled_tweets = ScheduledTweet.objects.filter(channel=obj.screen_name)
                for tweet in scheduled_tweets:
                    if tweet.status == ScheduledTweet.STATUS_ENABLED:
                        pt = tweet.periodic_task
                        pt.enabled = True
                        pt.save()
                obj.schedulingconfig.scheduling_enabled = True
                obj.schedulingconfig.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in SwitchStatusView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ScheduledTweetListView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DetailView):
    model = Channel
    context_object_name = "scheduled_tweet_list"

    def get_ajax(self, request, *args, **kwargs):
        objs = ScheduledTweet.objects.filter(channel=self.get_object())
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
                'text_excerpt': scheduled_tweet.get_excerpt() + "...",
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
            chan = Channel.objects.filter(screen_name=request.POST['channel'])[0]
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
            block.channel = chan
            block.save()
            response_data = {'result': "ok"}
        except Exception, e:
            logger.exception("Error while creating scheduled tweet")
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")

class ScheduledTweetDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = ScheduledTweet
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ScheduledPostsDetailView(DetailView):
    model = Channel
    template_name = "scheduling/index.html"
    context_object_name = "channel"


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