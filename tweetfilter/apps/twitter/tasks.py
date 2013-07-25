# -*- coding: utf-8 -*-

from celery import task
from apps.twitter.models import Tweet




@task(queue="tweets")
def store_tweet(data):
    try:
        tweet = Tweet()
        tweet.screen_name = data['user']['screen_name']
        tweet.text = data['text']
        tweet.tweet_id = data['id']
        tweet.source = data['source']
        tweet.mention_to = data['in_reply_to_screen_name']
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


@task(queue="tweets")
def send_tweet(tweet, twitterAPI):
    text = tweet.text
    if len(text) <= 140:
        twitterAPI.tweet(text)
    else:
        twitterAPI.tweet("%s.." % text[0:137])
    tweet.status = Tweet.STATUS_SENT
    tweet.save()
    return tweet