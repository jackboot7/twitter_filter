# Create your views here.
from django.contrib.sites.models import Site
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView, RedirectView, View
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
    """
    print "verifying"
    verification = twitter.verify_credentials()

    for k in verification:
        print "%s => %s" % (k,  verification[k])
    """
    redirect_url = auth['auth_url']+"&force_login=true"
    request.session['AUTH'] = {}
    request.session['AUTH']['OAUTH_TOKEN'] = auth['oauth_token']
    request.session['AUTH']['OAUTH_TOKEN_SECRET'] = auth['oauth_token_secret']

    print "TOKEN = %s" % request.session['AUTH']['OAUTH_TOKEN']
    print "SECRET = %s" % request.session['AUTH']['OAUTH_TOKEN_SECRET']

    return HttpResponseRedirect(redirect_url)

def auth_callback(request):

    oauth_verifier = request.GET['oauth_verifier']
    token = request.session['AUTH']['OAUTH_TOKEN']
    secret = request.session['AUTH']['OAUTH_TOKEN_SECRET']

    twitter = Twython(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET,
        token, secret)

    #final_step = twitter.get_authorized_tokens(oauth_verifier) # esta mierda no me retorna el screen_name

    # hacer el get (o post) a mano con requests para ver
    client = requests.Session()
    response = client.post(url="https://api.twitter.com/oauth/access_token", params={'oauth_verifier': oauth_verifier})
    print "response = %s" % response    # me retorna 401 (unauthorized)

    # obtener tokens finales
    # final_token = final_step['oauth_token']
    # final_secret = final_step['oauth_token_secret']

    """
    chan = Channel()
    chan.screen_name = name
    chan.oauth_token = final_token
    chan.oauth_secret = final_secret
    """

    return HttpResponse()