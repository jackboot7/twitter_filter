# Create your views here.
from django.views.generic.base import TemplateView

class AuthConfigView(TemplateView):
    template_name = 'auth/config.html'