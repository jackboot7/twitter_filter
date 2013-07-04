# Create your views here.
from django.contrib.sites.models import Site
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView, RedirectView, View
from django.views.generic.list import ListView
import requests
from twython.api import Twython
from apps.auth.models import Channel
from tweetfilter import settings
from tweetfilter.settings import TWITTER_APP_KEY, TWITTER_APP_SECRET

class AuthConfigView(TemplateView):
    template_name = 'auth/config.html'

def authenticate(request, screen_name):
    twitter = Twython(TWITTER_APP_KEY, TWITTER_APP_SECRET)

    callback = request.META.get('HTTP_REFERER', "") +\
               "auth/callback"

    auth = twitter.get_authentication_tokens(callback_url=callback)

    redirect_url = auth['auth_url']+"&force_login=true&screen_name="+screen_name
    request.session['AUTH'] = {}
    request.session['AUTH']['OAUTH_TOKEN'] = auth['oauth_token']
    request.session['AUTH']['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']

    return HttpResponseRedirect(redirect_url)

def auth_callback(request):

    oauth_verifier = request.GET['oauth_verifier']
    token = request.session['AUTH']['OAUTH_TOKEN']
    secret = request.session['AUTH']['OAUTH_TOKEN_SECRET']

    twitter = Twython(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET, token, secret)
    final_step = twitter.get_authorized_tokens(oauth_verifier) # esta mierda no me retorna el screen_name

    # obtener tokens finales
    final_token = final_step['oauth_token']
    final_secret = final_step['oauth_token_secret']
    name = final_step['screen_name']

    # Guardar canal en base de datos
    chan = Channel()
    chan.screen_name = name
    chan.oauth_token = final_token
    chan.oauth_secret = final_secret
    chan.save()

    return HttpResponse()


class ChannelListView(ListView):
    model = Channel
    context_object_name = "channel_list"
