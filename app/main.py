from twython import Twython

APP_KEY = 'gRzKIUiLxS51aO58Ucx7PA'
APP_SECRET = 'x4JGhz5aQVJTdxS8zzsENZhZyYW5TVbBbaiCt65aXU'

#twitter = Twython(APP_KEY, APP_SECRET)
#auth = twitter.get_authentication_tokens(callback_url='oob')

OAUTH_TOKEN = '1525868684-NY3YQFwsJel7vSSknG29AHo2VNX2IaWlQSvGGLZ'
OAUTH_TOKEN_SECRET = '7K1tawZ8GyRCFpxzqT2v8OvKGEkemAWOyuDP7YPr5jQ'

"""
print "Auth URL = %s" % auth['auth_url']
print "OAUTH_TOKEN = %s" % OAUTH_TOKEN
print "OAUTH_SECRET = %s" % OAUTH_TOKEN_SECRET
"""

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
print twitter.get_home_timeline()


#twitter.update_status(status='holaaaa :)')
#tl = twitter.get_home_timeline()
#print tl
