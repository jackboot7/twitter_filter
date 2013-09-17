# -*- coding: utf-8 -*-

import datetime
import logging
from django.conf import settings
from exceptions import Exception
from celery import task
from twython.exceptions import TwythonError
from twython.streaming.api import TwythonStreamer
from apps.accounts.models import  Channel
from apps.control.tasks import DelayedTask
from apps.filtering.models import BlockedUser, ChannelScheduleBlock, Replacement
from apps.twitter.api import ChannelAPI, Twitter
from apps.twitter.models import Tweet

logger = logging.getLogger('twitter')

class RetweetDelayedTask(DelayedTask):
    """
    DelayedTask class for the automatic retweet task.
    It should only run if now() is inside any of the account's timeblocks.
    It should delay execution until next available datetime otherwise.
    """
    screen_name = ""

    def __call__(self, *args, **kwargs):
        tweet = args[0]     # Tweet object

        if tweet is not None and tweet.status == Tweet.STATUS_APPROVED:
            # calculate nearest ETA and delay itself until then
            self.screen_name = tweet.mention_to
            eta = self.calculate_eta(tweet.type)
            if eta is None:
                logger.info("There are no blocks available for %s" % tweet.get_type_display())
                #print "There are no blocks available for %s" % tweet.get_type_display()
            else:
                countdown = (eta - datetime.datetime.now()).total_seconds()
                if countdown > 1:
                    logger.info("Tweet %s has been DELAYED until %s" % (tweet.tweet_id, eta))
                    #print "Tweet %s has been DELAYED until %s" % (tweet.tweet_id, eta)
                retweet.s().apply_async(args=args, kwargs=kwargs, countdown=countdown)
                return self.run(*args, **kwargs)
        else:
            pass    # nothing happens

    def set_channel_id(self, id):
        self.screen_name = id


    def calculate_eta(self, tweet_type):
        blocks = ChannelScheduleBlock.objects.filter(channel=self.screen_name)
        eta = datetime.datetime.max     # does this even work???
        #eta = blocks[0].next_datetime()
        if not len(blocks) > 0:
            # if there are no blocks, there are no restrictions, execute now.
            eta = datetime.datetime.now()

        for block in blocks:
            if not block.allows(tweet_type):
                continue
            block_eta = block.next_datetime()
            if block_eta < eta:
                eta = block_eta

        if eta == datetime.datetime.max:
            # time blocks found didn't allow tweet_type (dm or mention)
            return None
        else:
            return eta


class ChannelStreamer(TwythonStreamer):
    """
    TwythonStreamer subclass for a specific channel.
    Enables the stream, instantiating a filter_pipeline for each mention or DM received.
    """
    channel = {}
    twitter_api = {}

    def __init__(self, channel):
        super(ChannelStreamer, self).__init__(
            app_key=settings.TWITTER_APP_KEY, app_secret=settings.TWITTER_APP_SECRET,
            oauth_token=channel.oauth_token, oauth_token_secret=channel.oauth_secret)

        self.twitter_api = Twitter(key=settings.TWITTER_APP_KEY, secret=settings.TWITTER_APP_SECRET,
            token=channel.oauth_token, token_secret=channel.oauth_secret)

        self.channel = channel

    def on_success(self, data):
        # stores mentions and DMs only

        """
        print "new data from twitter!"
        print "data = %s" % json.dumps(data, sort_keys=True, indent=3)
        print ""
        print ""
        # """
        self.handle_data(data)

    def handle_data(self, data):
        if 'direct_message' in data:
            # Invokes subtask chain for storing and retweeting
            res = filter_pipeline_dm.apply_async([data])
        elif 'text' in data:
            for mention in data['entities']['user_mentions']:
                if self.channel.screen_name.lower() == mention['screen_name'].lower():
                    # Invokes subtask chain for storing and retweeting
                    res = filter_pipeline.apply_async([data, self.channel.screen_name])
        else:
            # should we handle the rest of the tweets?
            # Maybe store them for future use.
            pass

    def on_error(self, status_code, data):
        logger.error("Error en streaming")  # ampliar informacion

        #print "Error en streaming"
        #print status_code
        #print data
        self.disconnect()   # ???


@task(queue="streaming", ignore_result=True)
def stream_channel(chan_id):
    #print "Starting streaming for channel %s" % chan_id
    logger.info("Starting streaming for channel %s" % chan_id)
    try:
        chan = Channel.objects.filter(screen_name=chan_id)[0]
        streaming_task = chan.streaming_task
        #print "streaming task status = %s" % streaming_task.status
        #print "streaming task state = %s" % streaming_task.state
        #print "streaming task is ready? = %s" % streaming_task.ready()
        #from celery import current_app
        #inspect = current_app.control.inspect()
        #print "current active tasks = %s" % inspect.active()
        stream = ChannelStreamer(chan)
        stream.user(**{"with": "followings"})
        return True
    except Exception as e:
        #print "Error al iniciar streaming: %s" % e
        logger.exception("Error al iniciar streaming")
        return False


@task(queue="tweets", ignore_result=True)
def triggers_filter(tweet):
    if tweet is not None and tweet.status is not Tweet.STATUS_BLOCKED:
        #print "<%s>" % tweet.mention_to

        channel = Channel.objects.filter(screen_name=tweet.mention_to)[0]
        triggers = channel.get_triggers()
        try:
            for tr in triggers:
                if tr.occurs_in(tweet.strip_mentions()):
                    tweet.status = Tweet.STATUS_TRIGGERED
                    tweet.save()
                    logger.info("Marked #%s as TRIGGERED (found the trigger '%s')" % (tweet.tweet_id, tr.text))
                    #print "Marked #%s as TRIGGERED (found the trigger '%s')" % (tweet.tweet_id, tr.text)
                    break
            else:
                #print "Marked #%s as NOT TRIGGERED" % tweet.tweet_id
                logger.info("Marked #%s as NOT TRIGGERED" % tweet.tweet_id)
                tweet.status = Tweet.STATUS_NOT_TRIGGERED
                tweet.save()
        except Exception, e:
            logger.exception("error en trigger update")
            #print "error en trigger update: %s" % e

    return tweet


@task(queue="tweets", ignore_result=True)
def banned_words_filter(tweet):
    if tweet is not None and tweet.status == Tweet.STATUS_TRIGGERED:
        channel = Channel.objects.filter(screen_name=tweet.mention_to)[0]
        filters = channel.get_filters()
        try:
            for filter in filters:
                if filter.occurs_in(tweet.strip_mentions()):
                    tweet.status = Tweet.STATUS_BLOCKED
                    tweet.save()
                    #print "Blocked #%s (found the word '%s')" % (tweet.tweet_id, filter.text)
                    logger.info("Blocked #%s (found the word '%s')" % (tweet.tweet_id, filter.text))
                    break
            else:
                tweet.status = Tweet.STATUS_APPROVED
                tweet.save()

            return tweet
        except Exception, e:
            logger.exception("error en banned_words_filter")
            #print "error en banned_words_filter: %s" % e

    return tweet

@task(queue="tweets", ignore_result=True)
def filter_pipeline(data, screen_name):
    res =(
        store_tweet.s(data, screen_name) |
        is_user_allowed.s() |
        triggers_filter.s() |
        banned_words_filter.s() |
        #replacements_filter.s() |
        delay_retweet.s()).apply_async()
    return res

@task(queue="tweets", ignore_result=True)
def filter_pipeline_dm(data):
    res =(
        store_dm.s(data) |
        is_user_allowed.s() |
        triggers_filter.s() |
        banned_words_filter.s() |
        #replacements_filter.s() |
        delay_retweet.s()).apply_async()
    return res

@task(queue="tweets", ignore_result=True)
def is_user_allowed(tweet):
    if tweet is not None:
        from_user = tweet.screen_name
        #blocked_users = BlockedUser.objects.filter(channel=channel)
        blocked_users = BlockedUser.objects.filter(channel=tweet.mention_to)
        for user in blocked_users:
            if user.screen_name.lower() == from_user.lower():
                # user is blocked
                tweet.status = Tweet.STATUS_BLOCKED
                tweet.save()
                logger.info("Tweet %s marked as BLOCKED (sent from blacklisted user @%s)" % (tweet.tweet_id, user.screen_name))
                #print "Tweet %s marked as BLOCKED (sent from blacklisted user @%s)" % (tweet.tweet_id, user.screen_name)

    return tweet

@task(queue="tweets", base=RetweetDelayedTask, ignore_result=True)
def delay_retweet(tweet):
    pass

"""
@task(queue="tweets")
def replacements_filter(tweet):
    if tweet is not None and tweet.status == Tweet.STATUS_APPROVED:
        txt = tweet.text
        reps = Replacement.objects.filter(channel=tweet.mention_to)

        for rep in reps:
            if rep.occurs_in(tweet.text):
                txt = txt.replace(rep.text, rep.replace_with)

        tweet.retweeted_text = txt
    return tweet
"""

@task(queue="tweets", ignore_result=True, rate_limit="45/h")
def retweet(tweet):
    if tweet is not None and tweet.status == Tweet.STATUS_APPROVED:
        channel = Channel.objects.get(screen_name=tweet.mention_to)
        # Apply replacements
        reps = Replacement.objects.filter(channel=tweet.mention_to)
        txt = tweet.strip_channel_mention()
        for rep in reps:
            txt = rep.replace_in(txt)

        txt = "via @%s: %s" % (tweet.screen_name, txt)
        if len(txt) > 140:
            txt = "%s..." % txt[0:136]

        twitterAPI = ChannelAPI(channel)
        try:
            twitterAPI.tweet(txt)
            logger.info("Retweeted tweet #%s succesfully and marked it as SENT" % tweet.tweet_id)
            #print "Retweeted tweet #%s succesfully and marked it as SENT" % tweet.tweet_id

            tweet.status = Tweet.STATUS_SENT
            tweet.retweeted_text = txt
        except TwythonError, e:
            # parsear texto del error (detectar "update limit")
            tweet.status = Tweet.STATUS_NOT_SENT
            logger.exception("Tweet #%s NOT SENT" % tweet.tweet_id)
            #print "Tweet #%s NOT SENT" % tweet.tweet_id

        tweet.save()

    return tweet


@task(queue="tweets", ignore_result=True)
def store_tweet(data, channel_id):
    try:
        tweet = Tweet()
        tweet.screen_name = data['user']['screen_name']
        tweet.text = data['text']
        tweet.tweet_id = data['id']
        tweet.source = data['source']
        tweet.mention_to = channel_id
        tweet.type = Tweet.TYPE_MENTION
        tweet.save()
        logger.info(tweet)
        #print tweet
        #print "stored tweet %s as PENDING" % data['id']
        #print ""
        return tweet

    except Exception, e:
        logger.exception("Error trying to save tweet #%s" % data['id'])
        #print "Error trying to save tweet #%s: %s" % (data['id'], e)
        return None


@task(queue="tweets", ignore_result=True)
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
        print tweet
        #print "stored dm %s as PENDING" % data['id']
        print ""
        return tweet
    except Exception, e:
        logger.exception("Error trying to save dm #%s" % data['id'])
        #print "Error trying to save dm #%s: %s" % (data['id'], e)
        return None


@task(queue="tweets", ignore_result=True)
def send_tweet(tweet, twitterAPI):
    text = tweet.text
    if len(text) <= 140:
        twitterAPI.tweet(text)
    else:
        twitterAPI.tweet("%s.." % text[0:137])
    tweet.status = Tweet.STATUS_SENT
    tweet.save()
    return tweet