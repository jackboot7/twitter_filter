from django.conf.urls import *
from apps.channels.views import ChannelListView

urlpatterns = patterns('apps.auth.views',

    url(r'^list', ChannelListView.as_view()),

)