from exceptions import Exception
from celery import task
from apps.channels.backends import ChannelStreamer
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
                tweet.status = Tweet.STATUS_SENT
                tweet.save()
                print "Retweeted #%s (found the word '%s')" % (tweet.tweet_id, word)
                break
    except Exception, e:
        print "error en trigger update: %s" % e


@task(queue="tweets")
def triggers_filter(tweet, channel):
    triggers = channel.get_triggers()
    try:
        for tr in triggers:
            word = tr.text
            if word in tweet.text:

                tweet.status = Tweet.STATUS_RELEVANT
                tweet.save()
                print "Marked #%s as RELEVANT (found the trigger '%s')" % (tweet.tweet_id, word)
                break
        return tweet
    except Exception, e:
        print "error en trigger update: %s" % e


@task(queue="tweets")
def banned_words_filter(channel, tweet):
    filters = channel.get_filters()
    blocked = False
    try:
        for filter in filters:
            word = filter.text
            if word in tweet.text:
                tweet.status = Tweet.STATUS_BLOCKED
                tweet.save()
                blocked = True
                print "Blocked #%s (found the word '%s')" % (tweet.tweet_id, word)
                break

        if not blocked:
            tweet.status = Tweet.STATUS_APPROVED
            tweet.save()

        return tweet
    except Exception, e:
        print "error en banned_words_filter: %s" % e
    pass

@task(queue="tweets")
def filter_pipeline():
    pass