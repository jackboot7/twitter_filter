# -*- coding: utf-8 -*-
import sys
from twython.api import Twython
from twython.streaming.api import TwythonStreamer
from apps.channels.models import Channel
from apps.twitter.models import Tweet
from django.conf import settings


class Streamer(TwythonStreamer):
    filter_mode = ''

    def on_success(self, data):
        if 'text' in data:
            print "-------------------"
            print data
            #print data['text'].encode('utf-8')
            print "-------------------"
            print ""

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

class ChannelAPI(Twitter):
    def __init__(self, chan):
        super(ChannelAPI, self).__init__(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET, chan.oauth_token, chan.oauth_secret)

class ChannelStreamer(TwythonStreamer):
    channel = {}
    twitter_api = {}

    def __init__(self, channel):
        super(ChannelStreamer, self).__init__(
            app_key=settings.TWITTER_APP_KEY,
            app_secret=settings.TWITTER_APP_SECRET,
            oauth_token=channel.oauth_token,
            oauth_token_secret=channel.oauth_secret)
        self.twitter_api = Twitter(
            key=settings.TWITTER_APP_KEY,
            secret=settings.TWITTER_APP_SECRET,
            token=channel.oauth_token,
            token_secret=channel.oauth_secret
        )
        self.channel = channel

    def on_success(self, data):
        # stores mentions only
        #print "is %s in %s?" % ((self.channel.screen_name).lower(), data['text'].lower())
#        print "============================"
#        print "new data from twitter!"
#        print "data = %s" % data
#        print "============================"
#        print ""

        if 'text' in data and \
           "@" + (self.channel.screen_name).lower() in data['text'].lower():
            self.store(data)
            #self.trigger_update(data)

    def trigger_update(self, tweet):

        TRIGGER_WORDS = [u"trafico", u"tráfico"]
        try:
            for word in TRIGGER_WORDS:
                if word in tweet.text:
                    import re
                    regular_exp = re.compile(re.escape("@" + tweet.mention_to), re.IGNORECASE)
                    text = "via @" + tweet.screen_name + ":" + regular_exp.sub('', tweet.text)
                    self.twitter_api.tweet(text)
                    break

        except Exception, e:
            print "error en trigger update: %s" % e



    def on_error(self, status_code, data):
        print status_code
        print data
        self.disconnect()   # ???

    def store(self, data):
        try:
            tweet = Tweet()
            tweet.screen_name = data['user']['screen_name']
            tweet.text = data['text']
            tweet.tweet_id = data['id']
            tweet.source = data['source']
            tweet.mention_to = self.channel.screen_name
            tweet.save()
            print "stored tweet %s as PENDING" % data['id']
            self.trigger_update(tweet)

        except Exception, e:
            print "Error trying to save tweet #%s: %s" % (data['id'], e)