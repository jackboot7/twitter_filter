from django.conf.urls import *

from apps.notifications.views import NotificationListView


urlpatterns = patterns('apps.notifications.views',
    url(r'^history/', NotificationListView.as_view()),
)