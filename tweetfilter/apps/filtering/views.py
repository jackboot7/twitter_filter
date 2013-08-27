import datetime
from exceptions import Exception
import json
from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.views.generic import DetailView, View, DeleteView
from django.views.generic.edit import UpdateView
from apps.accounts.models import Channel
from apps.control.models import ScheduleBlock
from apps.filtering import tasks
from apps.filtering.models import BlockedUser, Trigger, Filter, ChannelScheduleBlock


#==========================
# Filtering Config
#==========================
class CheckStatusView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    """
    Returns filtering module status (is it enabled or disabled?)
    """
    model = Channel

    def get_ajax(self, request,  *args, **kwargs):
        obj = self.get_object()

        if obj.filteringconfig.retweets_enabled:
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
            if obj.filteringconfig.retweets_enabled:
                # disable
                obj.streaming_task.revoke(terminate=True)
                obj.filteringconfig.retweets_enabled = False
                obj.filteringconfig.save()
            else:
                # enable
                task = tasks.stream_channel.delay(obj.screen_name)
                obj.streaming_task = task   # tiene que haber un mejor lugar para guardar el task
                obj.save()
                obj.filteringconfig.retweets_enabled = True
                obj.filteringconfig.save()
            response_data = {'result': "ok"}
        except Exception as e:
            print " Error in SwitchStatusView: %s" % e
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


#==========================
# Trigger words
#==========================

class TriggerCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = Trigger

    def post_ajax(self, request, *args, **kwargs):

        try:
            chan = Channel.objects.filter(screen_name=request.POST['trigger_channel'])[0]
            trigger = Trigger()
            trigger.text = request.POST['trigger_text']
            trigger.channel = chan
            trigger.save()
            response_data = {'result': "ok"}
        except Exception, e:
            print "Error al crear trigger: %s" % e
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class TriggerListView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    model = Channel

    def get_ajax(self, request, *args, **kwargs):
        objs = Trigger.objects.filter(channel=self.get_object())

        json_list = []
        for trigger in objs:
            dict = model_to_dict(trigger)
            json_list.append(dict)

        return self.render_json_response(json_list)
        #return self.render_json_response(objs)


class TriggerDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = Trigger
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


#==========================
# Forbidden word filters
#==========================

class FilterCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = Filter

    def post_ajax(self, request, *args, **kwargs):

        try:
            chan = Channel.objects.filter(screen_name=request.POST['filter_channel'])[0]
            filter = Filter()
            filter.text = request.POST['filter_text']
            filter.channel = chan
            filter.save()
            response_data = {'result': "ok"}
        except Exception, e:
            print "Error al crear filter: %s" % e
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class FilterListView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    model = Channel

    def get_ajax(self, request, *args, **kwargs):
        objs = Filter.objects.filter(channel=self.get_object())

        json_list = []
        for trigger in objs:
            dict = model_to_dict(trigger)
            json_list.append(dict)

        return self.render_json_response(json_list)
        #return self.render_json_response(objs)


class FilterDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = Filter
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


#==========================
# Blocked users (blacklist)
#==========================

class BlockedUserListView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    model = Channel

    def get_ajax(self, request, *args, **kwargs):
        objs = BlockedUser.objects.filter(channel=self.get_object())

        json_list = []
        for user in objs:
            dict = model_to_dict(user)
            json_list.append(dict)

        return self.render_json_response(json_list)
        #return self.render_json_response(objs)


class BlockedUserDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = BlockedUser
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")

class BlockedUserAddView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = BlockedUser

    def post_ajax(self, request, *args, **kwargs):
        try:
            chan = Channel.objects.filter(screen_name=request.POST['blocked_user_channel'])[0]
            user = BlockedUser()
            user.screen_name = request.POST['blocked_user_name']
            user.channel = chan
            user.save()
            response_data = {'result': "ok"}
        except Exception, e:
            print "Error al bloquear usuario: %s" % e
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class TimeBlockListView(JSONResponseMixin, AjaxResponseMixin, DetailView):
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