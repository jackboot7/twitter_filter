from exceptions import Exception
import re
from celery import task
from apps.channels.backends import ChannelStreamer
from apps.twitter.api import ChannelAPI
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


"""
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
"""

@task(queue="tweets")
def triggers_filter(tweet, channel):
    from unidecode import unidecode
    triggers = channel.get_triggers()
    try:
        for tr in triggers:
            word = " %s " % unidecode(tr.text.lower())  # hace match con la palabra rodeada de espacios
            if word in unidecode(tweet.text.lower()):

                tweet.status = Tweet.STATUS_TRIGGERED
                tweet.save()
                print "Marked #%s as TRIGGERED (found the trigger '%s')" % (tweet.tweet_id, word)
                break
        else:
            tweet.status = Tweet.STATUS_NOT_TRIGGERED
            tweet.save()

        return tweet
    except Exception, e:
        print "error en trigger update: %s" % e


@task(queue="tweets")
def banned_words_filter(tweet, channel):
    from unidecode import unidecode
    filters = channel.get_filters()
    if tweet.status == Tweet.STATUS_TRIGGERED:
        try:
            for filter in filters:
                word = unidecode(filter.text.lower())
                if word in unidecode(tweet.text.lower()):
                    tweet.status = Tweet.STATUS_BLOCKED
                    tweet.save()
                    print "Blocked #%s (found the word '%s')" % (tweet.tweet_id, word)
                    break
            else:
                tweet.status = Tweet.STATUS_APPROVED
                tweet.save()

            return tweet
        except Exception, e:
            print "error en banned_words_filter: %s" % e

    return tweet

@task(queue="tweets")
def filter_pipeline(data, chan):
    from apps.twitter import tasks
    res =(
        tasks.store_tweet.s(data) |
        triggers_filter.s(channel=chan) |
        banned_words_filter.s(channel=chan) |
        retweet.s(channel=chan)).apply_async()
    return res

@task(queue="tweets")
def filter_pipeline_dm(data, chan):
    from apps.twitter import tasks
    res =(
        tasks.store_dm.s(data) |
        triggers_filter.s(channel=chan) |
        banned_words_filter.s(channel=chan) |
        retweet.s(channel=chan)).apply_async()
    return res

@task(queue="tweets")
def retweet(tweet, channel):
    if tweet.status == Tweet.STATUS_APPROVED:
        twitterAPI = ChannelAPI(channel)

        regular_exp = re.compile(re.escape("@" + tweet.mention_to), re.IGNORECASE)
        text = "via @" + tweet.screen_name + ":" + regular_exp.sub('', tweet.text)

        if len(text) > 140:
            text = "%s.." % text[0:137]

        twitterAPI.tweet(text)
        print "Retweeted tweet #%s succesfully and marked it as SENT" % tweet.tweet_id
        tweet.status = Tweet.STATUS_SENT
        tweet.retweeted_text = text
        tweet.save()

    return tweet