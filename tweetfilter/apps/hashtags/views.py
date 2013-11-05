import json
import logging
from braces.views import JSONResponseMixin, AjaxResponseMixin, CsrfExemptMixin
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
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
