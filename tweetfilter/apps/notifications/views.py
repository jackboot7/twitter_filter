from braces.views import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from apps.notifications.models import Notification

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/index.html"
    context_object_name = 'notifications'
    channel_added = None

    def get_queryset(self):
        qs = Notification.objects.filter(recipient=self.request.user).order_by("-time")
        paginator = Paginator(qs, 20)
        page = self.request.GET.get('page')
        try:
            notifications = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            notifications = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page.
            notifications = paginator.page(paginator.num_pages)

        return notifications


    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)
        return context
