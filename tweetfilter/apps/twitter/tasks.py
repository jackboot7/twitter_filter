from celery import task
from apps.channels.models import Channel
from apps.twitter.API import ChannelStreamer
from tweetfilter import settings

@task()
def stream_channel(chan):
    print "Started streaming for channel %s" % chan.screen_name
    stream = ChannelStreamer(chan)
    stream.user(**{"with": "followings"})

@task()
def print_holis():
    print "holis"