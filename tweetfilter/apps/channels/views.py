# -*- encoding: utf-8 -*-

import json
from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin
from django.http.response import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from apps.channels.models import Channel
from django.views.generic.edit import DeleteView, UpdateView
#from django.utils import simplejson as json

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
        self.get_object().stop_streaming()
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
        if obj.switch_status():
            response_data = {'result': "ok"}
        else:
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ChannelDetailView(DetailView):
    model = Channel
    template_name = "channels/index.html"
    context_object_name = "channel"