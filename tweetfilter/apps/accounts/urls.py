# -*- coding:utf-8 -*-

""" Urls for the accounts module. """

from django.conf.urls.defaults import patterns, url

from registration.views import RegistrationView
from apps.accounts.forms import RegistrationForm, LoginForm

urlpatterns = patterns('',
    #URL config for the login form.
    url(r'^login/',
        'django.contrib.auth.views.login',
        {'authentication_form': LoginForm},
        name='login'),

    # URL config for the registration form.
    url(r'^register/',
        #'registration.views.register',
        RegistrationView.as_view(form_class=RegistrationForm),
        name='registration')
)
