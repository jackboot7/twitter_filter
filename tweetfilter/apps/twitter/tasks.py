# -*- coding: utf-8 -*-

from billiard.exceptions import Terminated
from celery import task
from apps.channels.models import Channel
from apps.twitter.API import ChannelStreamer
from apps.twitter.models import Tweet
from tweetfilter import settings

@task()
def stream_channel(chan):
    print "Started streaming for channel %s" % chan.screen_name
    try:
        stream = ChannelStreamer(chan)
        stream.user(**{"with": "followings"})
    except Terminated:
        print "Stopped streaming for channel %s" % chan.screen_name

@task()
def store_tweet(data, mentioned):
    try:
        tweet = Tweet()
        tweet.screen_name = data['user']['screen_name']
        tweet.text = data['text']
        tweet.tweet_id = data['id']
        tweet.source = data['source']
        tweet.mention_to = mentioned
        tweet.save()
        print "stored tweet %s as PENDING" % data['id']
        return tweet

    except Exception, e:
        print "Error trying to save tweet #%s: %s" % (data['id'], e)
        return None

@task()
def trigger_update(tweet, twitterAPI):
    TRIGGER_WORDS = [u"trafico", u"tráfico"]
    try:
        for word in TRIGGER_WORDS:
            if word in tweet.text:
                import re
                regular_exp = re.compile(re.escape("@" + tweet.mention_to), re.IGNORECASE)
                text = "via @" + tweet.screen_name + ":" + regular_exp.sub('', tweet.text)
                twitterAPI.tweet(text)
                break

    except Exception, e:
        print "error en trigger update: %s" % e

