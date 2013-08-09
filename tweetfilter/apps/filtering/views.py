import json
from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from apps.channels.models import Channel, Trigger, Filter

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


class TriggerListView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DetailView):
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


class FilterListView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DetailView):
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