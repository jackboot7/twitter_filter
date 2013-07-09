from celery import task
from apps.channels.models import Channel
from apps.twitter.API import ChannelStreamer
from tweetfilter import settings

@task()
def stream_channel(chan):
    print "Started streaming for channel %s" % chan.screen_name
    stream = ChannelStreamer(
        app_key=settings.TWITTER_APP_KEY,
        app_secret=settings.TWITTER_APP_SECRET,
        oauth_token=chan.oauth_token,
        oauth_token_secret=chan.oauth_secret)
    stream.user(**{"with": "followings"})