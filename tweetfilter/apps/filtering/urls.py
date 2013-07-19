from django.conf.urls import *
from apps.filtering.views import TriggerDeleteView, TriggerCreateView, TriggerListView

urlpatterns = patterns('apps.filtering.views',

    url(r'^trigger/list', TriggerListView.as_view()),
    url(r'^trigger/delete/(?P<pk>\w+)', TriggerDeleteView.as_view()),
    url(r'^trigger/add', TriggerCreateView.as_view())

)