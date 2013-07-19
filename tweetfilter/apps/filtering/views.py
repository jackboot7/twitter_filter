import json
from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin
from django.http.response import HttpResponse
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, CreateView
from django.views.generic.list import ListView
from apps.filtering.models import Trigger

class TriggerCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = Trigger

    def post_ajax(self, request, *args, **kwargs):

        try:
            trigger = Trigger
            trigger.text = request.POST['trigger_text']
            trigger.channel = request.POST['trigger_channel']
            trigger.save()
            response_data = {'result': "ok"}
        except Exception, e:
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class TriggerListView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, ListView):
    model = Trigger

    def get_ajax(self, request, *args, **kwargs):
        objs = Trigger.objects.all()
        json_list = []
        for trigger in objs:
            json_list.append(trigger)

        return self.render_json_response(json_list)
        #return self.render_json_response(objs)


class TriggerDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = Trigger

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")