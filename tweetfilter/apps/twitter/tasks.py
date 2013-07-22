# -*- coding: utf-8 -*-

from billiard.exceptions import Terminated
from celery import task, states
from celery._state import current_task
from celery.exceptions import TaskRevokedError
from apps.channels.models import Channel
from apps.twitter.API import ChannelStreamer
from apps.twitter.models import Tweet


@task(queue="streaming")
def stream_channel(chan):
    print "Starting streaming for channel %s" % chan.screen_name
    try:
        stream = ChannelStreamer(chan)
        stream.user(**{"with": "followings"})

        #print "Streaming started"
        return True
        #current_task.update_state(state=states.STARTED) # no parece funcionar
    except Exception, e:    # ?????
        #print "Stopped streaming for channel %s" % chan.screen_name
        print "Error al iniciar streaming: %s" % e
        return False

@task(queue="tweets")
def store_tweet(data, mentioned):
    try:
        tweet = Tweet()
        tweet.screen_name = data['user']['screen_name']
        tweet.text = data['text']
        tweet.tweet_id = data['id']
        tweet.source = data['source']
        tweet.mention_to = mentioned
        tweet.type = Tweet.TYPE_MENTION
        tweet.save()
        print "stored tweet %s as PENDING" % data['id']
        return tweet

    except Exception, e:
        print "Error trying to save tweet #%s: %s" % (data['id'], e)
        return None

@task(queue="tweets")
def store_dm(dm, mentioned):
    data = dm['direct_message']
    try:
        tweet = Tweet()
        tweet.screen_name = data['sender']['screen_name']
        tweet.text = data['text']
        tweet.tweet_id = data['id']
        tweet.source = 'DM'
        tweet.mention_to = data['recipient_screen_name']
        tweet.type = Tweet.TYPE_DM
        tweet.save()
        print "stored dm %s as PENDING" % data['id']
        return tweet
    except Exception, e:
        print "Error trying to save dm #%s: %s" % (data['id'], e)
        return None


@task(queue="tweets")
def trigger_update(tweet, twitterAPI, channel):
    triggers = channel.get_triggers()
    try:
        for tr in triggers:
            word = tr.text
            if word in tweet.text:
                import re
                regular_exp = re.compile(re.escape("@" + tweet.mention_to), re.IGNORECASE)
                text = "via @" + tweet.screen_name + ":" + regular_exp.sub('', tweet.text)
                if len(text) <= 140:
                    twitterAPI.tweet(text)
                else:
                    twitterAPI.tweet("%s.." % text[0:137])
                print "Retweeted #%s (found the word '%s')" % (tweet.tweet_id, word)
                break
    except Exception, e:
        print "error en trigger update: %s" % e
