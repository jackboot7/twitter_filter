# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView
from twython.api import Twython
from apps.accounts.models import Channel


class HomeView(TemplateView):
    template_name = "accounts/index.html"

    def get(self, request, *args, **kwargs):
        channels = Channel.objects.all()
        return self.render_to_response({'channel_list': channels})


class ChannelAddedView(TemplateView):
    template_name = "accounts/index.html"

    def get(self, request, *args, **kwargs):
        channels = Channel.objects.all()
        return self.render_to_response({'channel_list': channels, 'channel_added': "true"})