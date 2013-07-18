import json
from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin
from django.http.response import HttpResponse
from django.views.generic.edit import DeleteView, CreateView
from django.views.generic.list import ListView
from apps.filtering.models import Trigger

class TriggerCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, CreateView):
    model = Trigger

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")

class TriggerListView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, ListView):
    model = Trigger

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")

class TriggerDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = Trigger

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")