# Create your views here.
from django.contrib.sites.models import Site
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView, RedirectView, View
from twython.api import Twython
from tweetfilter.settings import TWITTER_APP_KEY, TWITTER_APP_SECRET

class AuthConfigView(TemplateView):
    template_name = 'auth/config.html'


def authenticate(request, screen_name):
    site_url = request.META.get('HTTP_REFERER', "")
    twitter = Twython(TWITTER_APP_KEY, TWITTER_APP_SECRET)
    auth = twitter.get_authentication_tokens(callback_url='oob')
#        print "OAUTH_TOKEN = %s" % auth['oauth_token']
#        print "OAUTH_TOKEN_SECRET = %s" % auth['oauth_token_secret']
#        print "URL = %s" % auth['auth_url']
    #return super(AuthenticateRedirectView, self).get_redirect_url(url=auth['auth_url']) # +"&force_login=true"

    return HttpResponseRedirect(auth['auth_url']+"&force_login=true&screen_name="+screen_name)
