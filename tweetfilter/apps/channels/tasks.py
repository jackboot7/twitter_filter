from exceptions import Exception
import celery
from apps.channels.backends import ChannelStreamer

@celery.task(queue="streaming")
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


@celery.task(queue="tweets")
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