# -*- encoding: utf-8 -*-

import json
from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin
from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.base import View
from twython.api import Twython
from apps.accounts.models import Channel
from django.views.generic.edit import DeleteView


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
        #task = tasks.stream_channel.delay(chan.screen_name)
        #chan.streaming_task = task
        chan.init_streaming()
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
            retweets = channel.retweets_enabled
            scheduling = channel.scheduling_enabled
            hashtags  = channel.hashtags_enabled

            json_list.append({
                'screen_name': channel.screen_name,
                'filtering': u"Sí" if retweets else u"No",
                'scheduling': u"Sí" if scheduling else u"No",
                'hashtags': u"Sí" if hashtags else u"No",
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
        obj = self.get_object()
        self.delete(request)
        response_data = {"result": "ok"}
        return HttpResponse(json.dumps(response_data),
            content_type="application/json")
