import json
import logging
from braces.views import JSONResponseMixin, AjaxResponseMixin, CsrfExemptMixin
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from apps.accounts.models import Channel
from apps.hashtags.models import HashtagAdvertisement

logger = logging.getLogger('app')

class HashtagsDetailView(DetailView):
    model = Channel
    template_name = "hashtags/index.html"
    context_object_name = "channel"


class CheckStatusView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    """
    Returns scheduling module status (is it enabled or disabled?)
    """
    model = Channel

    def get_ajax(self, request,  *args, **kwargs):
        obj = self.get_object()

        if obj.hashtags_enabled:
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
            if obj.hashtags_enabled:
                # disable
                obj.hashtags_enabled = False
                obj.save()
            else:
                # enable
                obj.hashtags_enabled = True
                obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in hashtags.views.SwitchStatusView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class HashtagListView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DetailView):
    model = Channel
    context_object_name = "hashtag_list"

    def get_ajax(self, request, *args, **kwargs):
        objs = HashtagAdvertisement.objects.filter(channel=self.get_object())
        json_list = []

        for hashtag in objs:
            json_list.append(model_to_dict(hashtag))

        return self.render_json_response(json_list)

class HashtagCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = HashtagAdvertisement

    def post_ajax(self, request, *args, **kwargs):

        try:
            chan = Channel.objects.filter(screen_name=request.POST['channel'])[0]
            hashtag = HashtagAdvertisement()
            hashtag.text = request.POST['text']
            hashtag.quantity = request.POST['qty']
            hashtag.channel = chan
            hashtag.save()
            response_data = {'result': "ok"}
        except Exception, e:
            logger.exception("Error while creating scheduled tweet")
            response_data = {'result': e.args[0]}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")

class HashtagDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = HashtagAdvertisement
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class HashtagUpdateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    model = HashtagAdvertisement

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.text = request.POST['text']
            obj.quantity = request.POST['qty']
            obj.save()
            response_data = {'result': "ok"}
        except Exception, e:
            response_data = {'result': e.args[0]}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")
