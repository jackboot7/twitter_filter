# -*- coding: utf-8 -*-

from django.conf import settings
from twython import TwythonStreamer
from apps.twitter.api import Twitter
from apps.filtering import tasks

class ChannelStreamer(TwythonStreamer):
    """
    TwythonStreamer subclass for a specific channel.
    Enables the stream, instantiating a filter_pipeline for each mention or DM received.
    """
    channel = {}
    twitter_api = {}

    def __init__(self, channel):
        super(ChannelStreamer, self).__init__(
            app_key=settings.TWITTER_APP_KEY, app_secret=settings.TWITTER_APP_SECRET,
            oauth_token=channel.oauth_token, oauth_token_secret=channel.oauth_secret)

        self.twitter_api = Twitter(key=settings.TWITTER_APP_KEY, secret=settings.TWITTER_APP_SECRET,
            token=channel.oauth_token, token_secret=channel.oauth_secret)

        self.channel = channel

    def on_success(self, data):
        # stores mentions and DMs only
        print ""
        print ""
        print ""
        print "new data from twitter!"
        print "data = %s" % data

        self.handle_data(data)

    def handle_data(self, data):
        if 'direct_message' in data:
            print "\nGot DM!!!\n"
            # Invokes subtaskt chain for sotring and retweeting
            res = tasks.filter_pipeline_dm.apply_async([data, self.channel])
        elif 'text' in data:
            for mention in data['entities']['user_mentions']:
                if self.channel.screen_name.lower() == mention['screen_name'].lower():
                    print "\nGot Mention!!!\n"
                    # Invokes subtask chain for storing and retweeting
                    res = tasks.filter_pipeline.apply_async([data, self.channel])
        else:
            # We should manage the rest of the tweets?
            # Maybe store them for future use.
            pass

    def on_error(self, status_code, data):
        print "Error en streaming"
        print status_code
        print data
        self.disconnect()   # ???


