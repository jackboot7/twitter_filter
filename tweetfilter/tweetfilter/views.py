# -*- coding: utf-8 -*-
from django.views.generic import ListView

from braces.views import LoginRequiredMixin
from apps.accounts.models import Channel
from apps.notifications.models import Notification


class HomeView(LoginRequiredMixin, ListView):
    model = Channel
    template_name = "accounts/index.html"
    context_object_name = 'channel_list'
    channel_added = None

    def get_queryset(self):
        return Channel.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["channel_added"] = self.channel_added
        context["notification_list"] = Notification.objects.filter(recipient=self.request.user).order_by("-time")[0:7]
        self.request.session.set_expiry(0)   # Session expires after browser is closed
        return context
