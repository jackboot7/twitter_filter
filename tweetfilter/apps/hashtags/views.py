import json
import logging
from braces.views import JSONResponseMixin, AjaxResponseMixin, CsrfExemptMixin
from django.http.response import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from apps.accounts.models import Channel

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

        if obj.hashtagsconfig.hashtags_enabled:
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
            if obj.hashtagsconfig.hashtags_enabled:
                # disable
                obj.hashtagsconfig.hashtags_enabled = False
                obj.hashtagsconfig.save()
            else:
                # enable
                obj.hashtagsconfig.hashtags_enabled = True
                obj.hashtagsconfig.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in hashtags.views.SwitchStatusView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")
