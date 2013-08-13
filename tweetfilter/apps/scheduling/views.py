from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin
import datetime
from django.core.serializers import json
from django.http.response import HttpResponse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from apps.accounts.models import Channel
from apps.scheduling.models import ScheduledTweet

class ScheduledTweetkListView(CsrfExemptMixin, JSONResponseMixin,
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
                dias = "Todos"

            json_list.append({
                'id': scheduled_tweet.id,
                'date_time': scheduled_tweet.time + dias
            })

        return self.render_json_response(json_list)


class ScheduledTweetCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = ScheduledTweet

    def post_ajax(self, request, *args, **kwargs):

        try:
            chan = Channel.objects.filter(screen_name=request.POST['channel'])[0]
            block = ScheduledTweet()

            print "monday = %s" % request.POST['monday']
            print "tuesday = %s" % request.POST['tuesday']
            print "wednesday = %s" % request.POST['wednesday']
            print "thursday = %s" % request.POST['thursday']
            print "friday = %s" % request.POST['friday']
            print "saturday = %s" % request.POST['saturday']
            print "sunday = %s" % request.POST['sunday']

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
            print "Error al crear scheduled tweet: %s" % e
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


class ScheduledTweetkEditView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DetailView):
    model = ScheduledTweet
    context_object_name = "scheduled_tweet"

    def get_ajax(self, request, *args, **kwargs):
        json_obj = {}
        obj = self.get_object()

        json_obj.append({
            'id': obj.id,
            'time': obj.time,
            'monday': obj.monday,
            'tuesday': obj.tuesday,
            'wednesday': obj.wednesday,
            'thursday': obj.thursday,
            'friday': obj.friday,
            'saturday': obj.saturday,
            'sunday': obj.sunday,
        })

        return self.render_json_response(json_obj)

