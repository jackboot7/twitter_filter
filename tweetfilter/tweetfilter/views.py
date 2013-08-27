# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView
from twython.api import Twython
from apps.accounts.models import Channel

def test(request):

    APP_KEY = 'gRzKIUiLxS51aO58Ucx7PA'
    APP_SECRET = 'x4JGhz5aQVJTdxS8zzsENZhZyYW5TVbBbaiCt65aXU'

    # Token de acceso para OAUTH 2.0 (apps)
    ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAEHnRQAAAAAAPfgHk1BwUf9d5voSCWoQDPZ0KAQ%3DfyyndJwI0ETaidlgheWjxTfc7JnqPHvXzm8LGjIiZM'


    #
    # Prueba para obtener los permisos
    #

    # Step 1

    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens(callback_url='oob')

    print "OAUTH_TOKEN = %s" % auth['oauth_token']
    print "OAUTH_TOKEN_SECRET = %s" % auth['oauth_token_secret']

    print "URL = %s" % auth['auth_url']



    # Write down the tokens from the previous step
    """
    OAUTH_TOKEN = 'jk7OpbiWMs9Tri5cuLSKsMhfbVQoQLDj8et4AKsWbU'
    OAUTH_TOKEN_SECRET = 'qUuNGghPZBOCKUylgzQiKPMjY9Ua8ttfBfsJpOnPZc'
    PIN = '8155285'    # Get the PIN
    """

    # Step 2
    """
    twitter = Twython(APP_KEY, APP_SECRET,
        OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    final_step = twitter.get_authorized_tokens(PIN)
    print "OAUTH_TOKEN = %s" % final_step['oauth_token']
    print "OAUTH_TOKEN_SECRET = %s" % final_step['oauth_token_secret']
    """


    # Final Tokens (OAUTH 1.0)
    OAUTH_TOKEN = '1525868684-gYBZ43RKYCIJ6fAHujNlP5L9p14K5KXkaMXCsFQ'
    OAUTH_TOKEN_SECRET = 'FJTAK576ZT5bQYNnG5VpmRorZLPeZnMgbAl9ExA0'


    #
    # Prueba de leer twitter stream
    #

    """
    TRACK_WORDS = 'estoesunapruebacartelua'
    print "tracking: %s" % TRACK_WORDS

    stream = Streamer(APP_KEY, APP_SECRET,
        OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.filter_mode = 'medium'
    stream.user(**{"with": "followings"})
    """

    """
    TRACK_WORDS2 = 'estoesunapruebadelapidetwitter'
    stream2 = Streamer(APP_KEY, APP_SECRET,
        OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    #stream2.filter_mode = 'none'
    stream2.statuses.filter(track=TRACK_WORDS2)
    """




    # ---------------Testing------------------#
    """
    twitterAPI = Twitter(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    #tl = twitter.tweet('este texto es demasiado largo para twittear, no sé por qué no dejan que uno escriba más de 140 caracteres. Twitter es para maricas! (no se ofendan las maricas, pero es que es muy gay (no es que haya nada de malo con eso, no no...))')

    print "Comenzando flujo de prueba"
    stream_loop = StreamLoop(twitterAPI)
    filter_loop = FilterLoop(['Chavez'])
    retweet_loop = RetweetLoop(twitterAPI)


    while True:
        stream_loop.run()
        filter_loop.run()
        retweet_loop.run()

    """
    return None


class HomeView(TemplateView):
    template_name = "accounts/index.html"

    def get(self, request, *args, **kwargs):
        channels = Channel.objects.all()
        return self.render_to_response({'channel_list': channels})


class ChannelAddedView(TemplateView):
    template_name = "accounts/index.html"

    def get(self, request, *args, **kwargs):
        channels = Channel.objects.all()
        return self.render_to_response({'channel_list': channels, 'channel_added': "true"})