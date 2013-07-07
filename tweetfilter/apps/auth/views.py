# Create your views here.
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.base import TemplateView
from twython.api import Twython
from apps.channels.models import Channel
from tweetfilter import settings
from tweetfilter.settings import TWITTER_APP_KEY, TWITTER_APP_SECRET

class AuthConfigView(TemplateView):
    template_name = 'auth/config.html'

def authenticate(request):
    twitter = Twython(TWITTER_APP_KEY, TWITTER_APP_SECRET)

    callback = request.META.get('HTTP_REFERER', "") +\
               "auth/callback"

    auth = twitter.get_authentication_tokens(callback_url=callback)

    redirect_url = auth['auth_url']+"&force_login=true"
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

    return render_to_response("home/index.html", {'channel_added': 'true'},
        context_instance=RequestContext(request))


