# -*- encoding: utf-8 -*-

import json
from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin
import datetime
from django.http.response import HttpResponse
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from apps.channels.models import Channel, ChannelTimeBlock
from django.views.generic.edit import DeleteView, UpdateView
#from django.utils import simplejson as json
from apps.control.models import TimeBlock

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

class TimeBlockListView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DetailView):
    model = Channel
    context_object_name = "timeblock_list"

    def get_ajax(self, request, *args, **kwargs):
        objs = ChannelTimeBlock.objects.filter(channel=self.get_object())
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
    model = TimeBlock

    def post_ajax(self, request, *args, **kwargs):

        try:
            chan = Channel.objects.filter(screen_name=request.POST['timeblock_channel'])[0]
            block = ChannelTimeBlock()

            print "monday = %s" % request.POST['monday']
            print "tuesday = %s" % request.POST['tuesday']
            print "wednesday = %s" % request.POST['wednesday']
            print "thursday = %s" % request.POST['thursday']
            print "friday = %s" % request.POST['friday']
            print "saturday = %s" % request.POST['saturday']
            print "sunday = %s" % request.POST['sunday']

            block.start = request.POST['start']
            block.end = request.POST['end']
            block.monday = True if request.POST['monday'] == "1" else False
            block.tuesday = True if request.POST['tuesday'] == "1" else False
            block.wednesday = True if request.POST['wednesday'] == "1" else False
            block.thursday = True if request.POST['thursday'] == "1" else False
            block.friday = True if request.POST['friday'] == "1" else False
            block.saturday = True if request.POST['saturday'] == "1" else False
            block.sunday = True if request.POST['sunday'] == "1" else False
            block.channel = chan
            block.save()
            print "is now appliable? %s" % block.has_date_time(datetime.datetime.now())   #####
            response_data = {'result': "ok"}
        except Exception, e:
            print "Error al crear timeblock: %s" % e
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")

class TimeBlockDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = TimeBlock
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")