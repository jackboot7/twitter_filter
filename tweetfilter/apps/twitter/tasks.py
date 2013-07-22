# -*- coding: utf-8 -*-

from celery import task
from apps.twitter.models import Tweet




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
def store_dm(dm):
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



