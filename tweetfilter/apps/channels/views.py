# -*- encoding: utf-8 -*-

import json
from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.http.response import HttpResponse
from django.views.generic import ListView
from apps.channels.models import Channel
from django.views.generic.edit import DeleteView, UpdateView
#from django.utils import simplejson as json

class ChannelListView(JSONResponseMixin, AjaxResponseMixin, ListView):
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

class DeleteChannelView(DeleteView):
    model = Channel
    success_url = "/"

    def get_object(self, queryset=None):
        obj = super(DeleteChannelView, self).get_object()
        return obj

    def dispatch(self, *args, **kwargs):
        resp = super(DeleteChannelView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            response_data = {"result": "ok"}
            return HttpResponse(json.dumps(response_data),
                content_type="application/json")
        else:
            # redirige al success_url (no debería entrar por acá)
            return resp

class ChangeStatusView(UpdateView):
    model = Channel
    fields = ['status']

    def dispatch(self, *args, **kwargs):
        resp = super(ChangeStatusView, self).dispatch(*args, **kwargs)
        if self.request.is_ajax():
            obj = self.get_object()
            if obj.switch_status():
                response_data = {'result': "ok"}
            else:
                response_data = {'result': "fail"}

            return HttpResponse(json.dumps(response_data),
                content_type="application/json")
        else:
            # redirige al success_url (no debería entrar por acá)
            return resp



"""
def xhr_test(request, format):
    objs = Channel.objects.all()
    if request.is_ajax():
        data = serializers.serialize('json', objs)
        return HttpResponse(data,'json')
    else:
        return render_to_response('template.html', {'channel_list':objs}, context=...)
"""