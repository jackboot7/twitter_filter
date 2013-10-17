# -*- coding: utf-8 -*-

import datetime
import logging

from celery._state import current_task
from celery.signals import celeryd_init
from django.conf import settings
from exceptions import Exception
from celery import task
from django.core.cache import cache
from twython.exceptions import TwythonError
from twython.streaming.api import TwythonStreamer
from apps.accounts.models import  Channel
from apps.control.tasks import DelayedTask
from apps.filtering.models import BlockedUser, ChannelScheduleBlock, Replacement
from apps.twitter.api import ChannelAPI, Twitter
from apps.twitter.models import Tweet

TASK_EXPIRES = 900  # 15 min expiry


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
            channel = Channel.objects.get(screen_name=self.screen_name)
            logger = channel.get_logger()

            if channel.filteringconfig.scheduleblocks_enabled:
                eta = self.calculate_eta(tweet.type)
            else:
                eta = datetime.datetime.now()

            if eta is None:
                logger.info("There are no blocks available for %s" % tweet.get_type_display())
                pass
            else:
                countdown = (eta - datetime.datetime.now()).total_seconds()
                if countdown > 1:
                    logger.info("Tweet %s has been DELAYED until %s" % (tweet.tweet_id, eta))
                    pass
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
    task = {}

    def __init__(self, channel, task):
        super(ChannelStreamer, self).__init__(
            app_key=settings.TWITTER_APP_KEY, app_secret=settings.TWITTER_APP_SECRET,
            oauth_token=channel.oauth_token, oauth_token_secret=channel.oauth_secret)

        self.twitter_api = Twitter(key=settings.TWITTER_APP_KEY, secret=settings.TWITTER_APP_SECRET,
            token=channel.oauth_token, token_secret=channel.oauth_secret)
        self.task = task
        self.channel = channel

    def on_success(self, data):
        self.handle_data(data)

    def handle_data(self, data):
        if 'direct_message' in data:
            # Invokes subtask chain for storing and retweeting
            res = filter_pipeline_dm.apply_async([data])
        elif 'text' in data:
            for mention in data['entities']['user_mentions']:
                if self.channel.screen_name.lower() == mention['screen_name'].lower():
                    # Invokes subtask chain for storing, filtering and retweeting
                    res = filter_pipeline.apply_async([data, self.channel.screen_name])
        else:
            # should we handle the rest of the tweets?
            # Maybe store them for future use.
            pass

    def on_error(self, status_code, data):
        logger= self.channel.get_logger()
        logger.error("Error in streaming: %s: %s" % (status_code, data))  # ampliar informacion
        self.disconnect()
        cache.delete("streaming_lock_%s" % self.channel.screen_name)
        self.channel.filteringconfig.retweets_enabled = False
        self.channel.filteringconfig.save()
        # should retry??

    def disconnect(self):
        """Used to disconnect the streaming client manually"""
        logger= self.channel.get_logger()
        logger.info("Disconnected stream client for channel %s" % self.channel.screen_name)
        self.connected = False

@task(queue="streaming", ignore_result=True, default_retry_delay=60, max_retries=10)
def stream_channel(chan_id):
    chan = Channel.objects.filter(screen_name=chan_id)[0]
    stream_log = logging.getLogger('streaming')
    logger = chan.get_logger()

    try:
        message = "Starting streaming for %s" % chan.screen_name
        stream_log.info(message)
        logger.info(message)
        stream = ChannelStreamer(chan, current_task)
        stream.user(**{"with": "followings"})
        return True
    except Exception as e:
        message = "Error starting streaming for %s. Will retry later" % chan_id
        logger.exception(message)
        stream_log.exception(message)
        cache.delete("streaming_lock_%s" % chan_id)
        stream_channel.retry(exc=e, chan_id=chan_id)
        return False


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def filter_pipeline(data, screen_name):
    res =(
        store_tweet.s(data, screen_name) |
        is_user_allowed.s() |
        triggers_filter.s() |
        banned_words_filter.s() |
        #replacements_filter.s() |
        delay_retweet.s()).apply_async()
    return res

@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
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
def store_tweet(data, channel_id):
    channel = Channel.objects.get(screen_name=channel_id)
    logger = channel.get_logger()
    try:
        import HTMLParser
        html = HTMLParser.HTMLParser()

        tweet = Tweet()
        tweet.screen_name = data['user']['screen_name']
        tweet.text = html.unescape(data['text'])
        tweet.tweet_id = data['id']
        tweet.source = data['source']
        tweet.mention_to = channel_id
        tweet.type = Tweet.TYPE_MENTION
        tweet.save()
        logger.info(tweet.__unicode__())
        return tweet
    except Exception, e:
        logger.exception("Error trying to save tweet #%s" % data['id'])
        return None


@task(queue="tweets", ignore_result=True)
def store_dm(dm):
    data = dm['direct_message']
    channel = Channel.objects.get(screen_name=data['recipient_screen_name'])
    logger = channel.get_logger()
    try:
        import HTMLParser
        html = HTMLParser.HTMLParser()

        tweet = Tweet()
        tweet.screen_name = data['sender']['screen_name']
        tweet.text = html.unescape(data['text'])
        tweet.tweet_id = data['id']
        tweet.source = 'DM'
        tweet.mention_to = data['recipient_screen_name']
        tweet.type = Tweet.TYPE_DM
        tweet.save()
        logger.info(tweet)
        return tweet
    except Exception, e:
        logger.exception("Error trying to save dm #%s" % data['id'])
        return None


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def triggers_filter(tweet):
    if tweet is not None and tweet.status is not Tweet.STATUS_BLOCKED:
        channel = Channel.objects.filter(screen_name=tweet.mention_to)[0]

        # if feature is disabled, pass the tweet
        if not channel.filteringconfig.triggers_enabled:
            tweet.status = Tweet.STATUS_TRIGGERED
            tweet.save()
            return tweet

        logger = channel.get_logger()
        triggers = channel.get_triggers()
        try:
            for tr in triggers:
                if tr.occurs_in(tweet.strip_channel_mention()):
                    tweet.status = Tweet.STATUS_TRIGGERED
                    tweet.save()
                    logger.info("Marked #%s as TRIGGERED (found the trigger '%s')" %
                                (tweet.tweet_id, tr.text))
                    break
            else:
                logger.info("Marked #%s as NOT TRIGGERED" % tweet.tweet_id)
                tweet.status = Tweet.STATUS_NOT_TRIGGERED
                tweet.save()
        except Exception, e:
            logger.exception("error en triggers filter")
            pass
    return tweet


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def banned_words_filter(tweet):
    if tweet is not None and tweet.status == Tweet.STATUS_TRIGGERED:
        channel = Channel.objects.filter(screen_name=tweet.mention_to)[0]

        # if feature is disabled, pass the tweet
        if not channel.filteringconfig.filters_enabled:
            tweet.status = Tweet.STATUS_APPROVED
            tweet.save()
            return tweet

        logger = channel.get_logger()
        filters = channel.get_filters()
        try:
            for filter in filters:
                if filter.occurs_in(tweet.strip_channel_mention()):
                    tweet.status = Tweet.STATUS_BLOCKED
                    tweet.save()
                    logger.info("BLOCKED tweet #%s (found the word '%s')" %
                                (tweet.tweet_id, filter.text))
                    break
            else:
                tweet.status = Tweet.STATUS_APPROVED
                tweet.save()

            return tweet
        except Exception, e:
            logger.exception("error en banned_words_filter")
            pass
    return tweet


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def is_user_allowed(tweet):
    if tweet is not None:
        from_user = tweet.screen_name
        channel = Channel.objects.get(screen_name=tweet.mention_to)

        # if feature is disabled, pass the tweet
        if not channel.filteringconfig.blacklist_enabled:
            return tweet

        logger = channel.get_logger()
        blocked_users = BlockedUser.objects.filter(channel=tweet.mention_to)
        for user in blocked_users:
            if user.screen_name.lower() == from_user.lower():
                # user is blocked
                tweet.status = Tweet.STATUS_BLOCKED
                tweet.save()
                logger.info("Tweet %s marked as BLOCKED (sent from blacklisted user @%s)" %
                            (tweet.tweet_id, user.screen_name))
    return tweet


@task(queue="tweets", base=RetweetDelayedTask, ignore_result=True, expires=TASK_EXPIRES)
def delay_retweet(tweet):
    pass


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def retweet(tweet, txt=None):
    LOCK_EXPIRE = 60 * 5    # Lock expires in 5 minutes
    DELAY_DELTA = 60        # allows updating status each minute per channel

    if tweet is not None and tweet.status == Tweet.STATUS_APPROVED:
        channel = Channel.objects.get(screen_name=tweet.mention_to)
        log = channel.get_logger()
        # Apply replacements
        if txt is None:
            txt = tweet.strip_channel_mention()

        if channel.filteringconfig.replacements_enabled:
            reps = Replacement.objects.filter(channel=tweet.mention_to)

            for rep in reps:
                txt = rep.replace_in(txt)

            txt = "via @%s: %s" % (tweet.screen_name, txt)
            if len(txt) > 140:
                txt = "%s..." % txt[0:136]

        if cache.add("retweet_lock_%s" % channel.screen_name, "true", LOCK_EXPIRE):  # acquire lock
            try:
                last = cache.get('%s_last_tweet' % channel.screen_name)
                now = datetime.datetime.now()

                if last is not None and (now - last).total_seconds() < DELAY_DELTA:
                    # if it's not first tweet and last tweet is recent, delay.
                    eta = last + datetime.timedelta(seconds=DELAY_DELTA)
                    countdown = (eta - now).total_seconds()
                    if countdown < TASK_EXPIRES:
                        cache.set('%s_last_tweet' % channel.screen_name, eta)
                        update_status.s().apply_async(args=[channel.screen_name, tweet, txt],
                            countdown=countdown)
                        log.debug("Tweet %s will be sent in %s seconds" %
                                  (tweet.tweet_id, countdown))
                    else:
                        tweet.status = Tweet.STATUS_NOT_SENT
                        log.info("Tweet %s marked as NOT SENT (Too many messages in queue)" %
                                 tweet.tweet_id)
                else:
                    # send now
                    update_status.s().apply_async(args=[channel.screen_name, tweet, txt],
                        countdown=0)
                    cache.set('%s_last_tweet' % channel.screen_name, now)
            finally:
                cache.delete("retweet_lock_%s" % channel.screen_name)    # release lock
        else:
            retweet.s().apply_async(args=[tweet, txt], countdown=5)
            # retry

    return tweet


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def update_status(channel_id, tweet, txt):
    channel = Channel.objects.get(screen_name=channel_id)
    logger = channel.get_logger()

    try:
        if channel.filteringconfig.retweets_enabled:
            api = ChannelAPI(channel)
            api.tweet(txt)
            logger.info("Retweeted tweet #%s succesfully and marked it as SENT" % tweet.tweet_id)
            tweet.status = Tweet.STATUS_SENT
            tweet.retweeted_text = txt
            tweet.save()
        else:
            logger.info("Tweet #%s marked as NOT_SENT (channel was disabled)" % tweet.tweet_id)
            tweet.status = Tweet.STATUS_NOT_SENT
            tweet.retweeted_text = txt
            tweet.save()
    except TwythonError, e:
        if "update limit" in e.message:
            # save event for statistics
            pass
        if "duplicate" in e.message:
            pass
        tweet.status = Tweet.STATUS_NOT_SENT
        logger.exception("Tweet #%s NOT SENT" % tweet.tweet_id)


@celeryd_init.connect
def initialize_streaming_tasks(sender=None, conf=None, **kwargs):
    channels = Channel.objects.all()
    for chan in channels:
        if chan.filteringconfig.retweets_enabled:
            chan.init_streaming()
