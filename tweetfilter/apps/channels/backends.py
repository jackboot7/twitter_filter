from celery import chain
from django.conf import settings
from twython import TwythonStreamer
from apps.twitter.api import Twitter
from apps.channels import tasks as channel_tasks
from apps.twitter import tasks as twitter_tasks


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

                    res = chain(
                        twitter_tasks.store_tweet.s(data, self.channel.screen_name),
                        channel_tasks.trigger_update.s(twitterAPI=self.twitter_api, channel=self.channel)).apply_async()


        if 'direct_message' in data:    # DM
            print "\nGot DM!!!\n"
            # Invokes subtask chain for storing and retweeting
            #print "hubo mention (%s)" % self.channel.screen_name
            res = chain(
                twitter_tasks.store_dm.s(data, self.channel.screen_name),
                channel_tasks.trigger_update.s(twitterAPI=self.twitter_api, channel=self.channel)).apply_async()


    def on_error(self, status_code, data):
        print "Error en streaming"
        print status_code
        print data
        self.disconnect()   # ???