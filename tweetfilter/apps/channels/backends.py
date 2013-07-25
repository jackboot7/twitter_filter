from celery import chain
from django.conf import settings
from twython import TwythonStreamer
from apps.twitter.api import Twitter



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
        # stores mentions and DMs only
        print ""
        print "============================"
        print "new data from twitter!"
        print "data = %s" % data
        print "============================"
        print ""

        if 'text' in data:      # regular tweet
            for mention in data['entities']['user_mentions']:
                if self.channel.screen_name.lower() == mention['screen_name'].lower():
                    #current channel is mentioned

                    print "\nGot mention!!!\n"
                    # Invokes subtask chain for storing and retweeting
                    from . import tasks
                    res = tasks.filter_pipeline.apply_async([data, self.channel])

        if 'direct_message' in data:    # DM
            print "\nGot DM!!!\n"
            # Invokes subtask chain for storing and retweeting
            from . import tasks
            res = tasks.filter_pipeline_dm.apply_async([data, self.channel])


    def on_error(self, status_code, data):
        print "Error en streaming"
        print status_code
        print data
        self.disconnect()   # ???