from django.conf.urls import *
from apps.auth.views import AuthConfigView

urlpatterns = patterns('apps.auth.views',

    url(r'^config', AuthConfigView.as_view()),
    url(r'^authenticate/(\w*)', 'authenticate'),
    url(r'^callback', 'auth_callback')
)