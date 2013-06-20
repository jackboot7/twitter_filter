from twython import Twython
from apps.tweets.API import Streamer, Twitter


APP_KEY = 'gRzKIUiLxS51aO58Ucx7PA'
APP_SECRET = 'x4JGhz5aQVJTdxS8zzsENZhZyYW5TVbBbaiCt65aXU'

# Token de acceso para OAUTH 2.0 (apps)
ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAEHnRQAAAAAAPfgHk1BwUf9d5voSCWoQDPZ0KAQ%3DfyyndJwI0ETaidlgheWjxTfc7JnqPHvXzm8LGjIiZM'


#
# Prueba para obtener los permisos
#

# Step 1
"""
twitter = Twython(APP_KEY, APP_SECRET)
auth = twitter.get_authentication_tokens(callback_url='oob')

print "OAUTH_TOKEN = %s" % auth['oauth_token']
print "OAUTH_TOKEN_SECRET = %s" % auth['oauth_token_secret']

print "URL = %s" % auth['auth_url']
"""


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
stream.statuses.filter(track=TRACK_WORDS)
"""

"""
TRACK_WORDS2 = 'estoesunapruebadelapidetwitter'
stream2 = Streamer(APP_KEY, APP_SECRET,
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
#stream2.filter_mode = 'none'
stream2.statuses.filter(track=TRACK_WORDS2)
"""


# ---------------Testing------------------#

twitter = Twitter(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
tl = twitter.get_messages()
print tl