# -*- encoding: utf-8 -*-

import json
from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin
import datetime
from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from twython.api import Twython
from apps.accounts import tasks
from apps.accounts.models import Channel, ChannelScheduleBlock
from django.views.generic.edit import DeleteView, UpdateView
from apps.control.models import ScheduleBlock


class TwitterAuthenticationView(View):
    def get(self, request, *args, **kwargs):
        """
        Calls the twitter endpoint for authentication
        """
        twitter = Twython(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET,
            auth_endpoint='authorize')
        callback = "http://" + RequestSite(request).domain + "/accounts/auth_callback"
        auth = twitter.get_authentication_tokens(callback_url=callback)
        redirect_url = auth['auth_url']+"&force_login=true&screen_name="

        request.session['AUTH'] = {}
        request.session['AUTH']['OAUTH_TOKEN'] = auth['oauth_token']
        request.session['AUTH']['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']

        return HttpResponseRedirect(redirect_url)


class AuthCallbackView(View):
    def get(self, request, *args, **kwargs):
        """
        Callback function when returning from twitter authentication form
        """
        # Get the provisional tokens
        oauth_verifier = request.GET['oauth_verifier']
        token = request.session['AUTH']['OAUTH_TOKEN']
        secret = request.session['AUTH']['OAUTH_TOKEN_SECRET']

        twitter = Twython(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET, token, secret)
        final_step = twitter.get_authorized_tokens(oauth_verifier)

        # Get the final tokens
        final_token = final_step['oauth_token']
        final_secret = final_step['oauth_token_secret']
        name = final_step['screen_name']

        # Create new channel object
        chan = Channel()
        chan.screen_name = name
        chan.oauth_token = final_token
        chan.oauth_secret = final_secret
        chan.save()

        #initializes streaming process
        task = tasks.stream_channel.delay(chan.screen_name)
        chan.streaming_task = task
        chan.save()

        return HttpResponseRedirect(reverse("channel_added"))


class ChannelListView(JSONResponseMixin, AjaxResponseMixin, ListView):
    """
    Return json list with all existing channels
    """
    model = Channel
    context_object_name = "channel_list"

    def get_ajax(self, request, *args, **kwargs):
        objs = Channel.objects.all()
        json_list = []

        for channel in objs:
            last_tweet = channel.get_last_update()
            excerpt = last_tweet.get_excerpt() if last_tweet is not None else ""
            json_list.append({
                'screen_name': channel.screen_name,
                'last_tweet': excerpt,
                'status' : channel.get_status_display()
            })

        return self.render_json_response(json_list)


class DeleteChannelView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    """
    Deletes a channel via Ajax
    """
    model = Channel
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #self.get_object().stop_streaming()
        self.get_object().streaming_task.revoke(terminate=True)
        self.delete(request)
        response_data = {"result": "ok"}
        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ChangeStatusView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Switches a channel status: if it's enabled, it becomes disabled, and viceversa.
    """
    model = Channel
    fields = ['status']

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.switch_status()
        try:
            if obj.status == Channel.STATUS_ENABLED:
                task = tasks.stream_channel.delay(obj.screen_name)
                obj.streaming_task = task   # tiene que haber un mejor lugar para guardar el task
                obj.save()
            else:
                obj.streaming_task.revoke(terminate=True)
            response_data = {'result': "ok"}
        except Exception as e:
            print "Error en ChangeStatus: %s" % e
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ChannelDetailView(DetailView):
    model = Channel
    template_name = "accounts/index.html"
    context_object_name = "channel"


class TimeBlockListView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DetailView):
    model = Channel
    context_object_name = "timeblock_list"

    def get_ajax(self, request, *args, **kwargs):
        objs = ChannelScheduleBlock.objects.filter(channel=self.get_object())
        json_list = []

        for timeblock in objs:
            dias = ""
            if timeblock.monday:
                dias = "Lun "
            if timeblock.tuesday:
                dias += "Mar "
            if timeblock.wednesday:
                dias += "Mie "
            if timeblock.thursday:
                dias += "Jue "
            if timeblock.friday:
                dias += "Vie "
            if timeblock.saturday:
                dias += "Sab "
            if timeblock.sunday:
                dias += "Dom "
            if len(dias) == 28:
                dias = "Todos"

            json_list.append({
                'id': timeblock.id,
                'start': timeblock.start,
                'end': timeblock.end,
                'days': dias
                #'days' : ????
            })

        return self.render_json_response(json_list)


class TimeBlockCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = ScheduleBlock

    def post_ajax(self, request, *args, **kwargs):

        try:
            chan = Channel.objects.filter(screen_name=request.POST['timeblock_channel'])[0]
            block = ChannelScheduleBlock()

            print "monday = %s" % request.POST['monday']
            print "tuesday = %s" % request.POST['tuesday']
            print "wednesday = %s" % request.POST['wednesday']
            print "thursday = %s" % request.POST['thursday']
            print "friday = %s" % request.POST['friday']
            print "saturday = %s" % request.POST['saturday']
            print "sunday = %s" % request.POST['sunday']

            block.start = datetime.datetime.strptime(request.POST['start'], "%H:%M").time()
            block.end = datetime.datetime.strptime(request.POST['end'], "%H:%M").time()

            block.monday = True if request.POST['monday'] == "1" else False
            block.tuesday = True if request.POST['tuesday'] == "1" else False
            block.wednesday = True if request.POST['wednesday'] == "1" else False
            block.thursday = True if request.POST['thursday'] == "1" else False
            block.friday = True if request.POST['friday'] == "1" else False
            block.saturday = True if request.POST['saturday'] == "1" else False
            block.sunday = True if request.POST['sunday'] == "1" else False
            block.channel = chan
            block.save()
            print "is now appliable? %s" % block.has_datetime(datetime.datetime.now())   #####
            response_data = {'result': "ok"}
        except Exception, e:
            print "Error al crear timeblock: %s" % e
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class TimeBlockDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = ScheduleBlock
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")

    
class ScheduledPostsDetailView(DetailView):
    model = Channel
    template_name = "accounts/scheduled_posts.html"
    context_object_name = "channel"