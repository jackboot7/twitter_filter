from twython.api import Twython
from twython.streaming.api import TwythonStreamer


class Streamer(TwythonStreamer):
    filter_mode = ''

    def on_success(self, data):
        if 'text' in data:
            print "-------------------"
            print data
            #print data['text'].encode('utf-8')
            print "-------------------"

    def on_error(self, status_code, data):
        print status_code
        print data
        self.disconnect()   # ???

class Twitter():
    app_key = ''
    app_secret = ''
    oauth_token = ''
    oauth_token_secret = ''
    connector = {}

    def __init__(self, key, secret, token, token_secret):
        self.app_key = key
        self.app_secret = secret
        self.oauth_token = token
        self.oauth_token_secret = token_secret
        self.connector = Twython(key, secret, token, token_secret)

    def get_streamer(self, token, secret):
        return Streamer(self.app_key, self.app_secret, token, secret)

    def get_timeline(self):
        return self.connector.get_user_timeline()

    def get_mentions_since(self, since):
        return self.connector.get_mentions_timeline(since_id=since)

    def get_mentions(self):
        return self.connector.get_mentions_timeline()

    def get_messages(self):
        return self.connector.get_direct_messages()

    def tweet(self, txt):
        if len(txt) <= 140:
            self.connector.update_status(status=txt)
        else:
            raise Exception('message over 140 characters')