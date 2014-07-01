# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django import forms
from django.core.urlresolvers import reverse_lazy
from braces.forms import UserKwargModelFormMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from registration.forms import RegistrationFormUniqueEmail, RegistrationFormTermsOfService


# Use this tuple to config the Bootstrap Helper Attributes from crispy_forms
bootstrap_helper_attr = (True, True)


class LoginForm(AuthenticationForm):
    """
    Same fields as original login form.
    Extended to add crispy helpers.
    """
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-login-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'

        # Bootstrap Helper Attributes
        self.helper.html5_required, self.helper.help_text_inline = bootstrap_helper_attr

        self.helper.add_input(Submit('submit', 'Login'))
        super(LoginForm, self).__init__(*args, **kwargs)


class UserRegistrationForm(RegistrationFormUniqueEmail, RegistrationFormTermsOfService):
    """
    Registration form for Users
    """
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-user-registration-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'user_registration'

        # Bootstrap Helper Attributes
        self.helper.html5_required, self.helper.help_text_inline = bootstrap_helper_attr

        self.helper.add_input(Submit('submit', 'Submit'))
        super(UserRegistrationForm, self).__init__(*args, **kwargs)


class PasswordChangeForm(DjangoPasswordChangeForm):
    """
    Change Passwords for users
    """
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-change-password-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'password_change'

        # Bootstrap Helper Attributes
        self.helper.html5_required, self.helper.help_text_inline = bootstrap_helper_attr

        self.helper.add_input(Submit('submit', 'Submit'))
        super(PasswordChangeForm, self).__init__(*args, **kwargs)


class PasswordResetForm(DjangoPasswordResetForm):
    """
    Reset password using an email field.
    """
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-reset-password-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'password_reset'

        # Bootstrap Helper Attributes
        self.helper.html5_required, self.helper.help_text_inline = bootstrap_helper_attr

        self.helper.add_input(Submit('submit', 'Submit'))
        super(PasswordResetForm, self).__init__(*args, **kwargs)
