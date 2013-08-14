# -*- coding: utf-8 -*-

from django.conf import settings

from django import forms
from django.contrib.auth import forms as auth_forms


from registration.forms import RegistrationFormUniqueEmail, RegistrationFormTermsOfService

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

bootstrap_helper_attr = (True, True)


class RegistrationForm(RegistrationFormUniqueEmail, RegistrationFormTermsOfService):
    """ Adds crispy_forms helpers to a mashup of django-registration forms"""

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-registration-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'registration'

        # Bootstrap Helper attrs.
        self.helper.html5_required, self.helper.help_text_inline = bootstrap_helper_attr

        self.helper.add_input(Submit('submit', 'Submit'))
        super(RegistrationForm, self).__init__(*args, **kwargs)


class LoginForm(auth_forms.AuthenticationForm):
    """ Same fields as Django's login form. Extended to add crispy_forms helpers"""

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-login-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'

        #Bootstrap Helper attrs.
        self.helper.html5_required, self.helper.help_text_inline = bootstrap_helper_attr

        self.helper.add_input(Submit('submit', 'Login'))
        super(LoginForm, self).__init__(*args, **kwargs)


#class UpdateProfileForm(forms.ModelForm):
#
#    class Meta:
#        model = settings.AUTH_USER_MODEL
#        fields = ['first_name', 'last_name', 'email']
#
#    def __init__(self, *args, **kwargs):
#        super(UpdateProfileForm, self).__init__(*args, **kwargs)
#

class PasswordChangeForm(auth_forms.PasswordChangeForm):
    """ Adds crispy_forms helpers to auth.forms.PasswordChangeForm"""

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)


class PasswordResetForm(auth_forms.PasswordResetForm):
    """ Adds crispy_forms helpers to auth.forms.PasswordChangeForm"""
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

# End?
