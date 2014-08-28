# -*- coding: utf-8 -*-

import datetime
import logging
from random import randint
from exceptions import Exception

from celery._state import current_task
from celery import task
from celery.signals import task_revoked, task_failure, celeryd_after_setup, celeryd_init, worker_init, worker_shutdown
from django.conf import settings
from django.core.cache import cache
from twython.streaming.api import TwythonStreamer

from apps.accounts.models import Channel
from apps.control.models import UpdateLimit
from apps.control.tasks import DelayedTask
from apps.filtering.models import BlockedUser, ChannelScheduleBlock, Replacement
from apps.hashtags.models import HashtagAdvertisement, HashtagAppliance
from apps.twitter.api import ChannelAPI, Twitter
from apps.twitter.models import Tweet

"""
Filtering tasks workflow:

store_tweets -->
triggers_filter -->
is_user_allowed -->
banned_words_filter -->
delay_retweet -->
retweet -->
update_status
"""

TASK_EXPIRES = 900  # 15 min expiry


##################################
# Logging tasks
##################################

@task(queue="logging", ignore_result=True)
def channel_log(message, level, channel_id):
    logger = logging.LoggerAdapter(logging.getLogger("twitter"), {
        'screen_name': channel_id
    })
    logger.log(level=level, msg=message)
    return


@task(queue="logging", ignore_result=True)
def channel_log_debug(message, channel_id):
    logger = logging.LoggerAdapter(logging.getLogger("twitter"), {
        'screen_name': channel_id
    })
    logger.debug(message)
    return


@task(queue="logging", ignore_result=True)
def channel_log_info(message, channel_id):
    logger = logging.LoggerAdapter(logging.getLogger("twitter"), {
        'screen_name': channel_id
    })
    logger.info(message)
    return


@task(queue="logging", ignore_result=True)
def channel_log_warning(message, channel_id):
    logger = logging.LoggerAdapter(logging.getLogger("twitter"), {
        'screen_name': channel_id
    })
    logger.warning(message)
    return


@task(queue="logging", ignore_result=True)
def channel_log_exception(message, channel_id):
    logger = logging.LoggerAdapter(logging.getLogger("twitter"), {
        'screen_name': channel_id
    })
    logger.error(message)
    return


@task(queue="logging", ignore_result=True)
def channel_log_error(message, channel_id):
    logger = logging.LoggerAdapter(logging.getLogger("twitter"), {
        'screen_name': channel_id
    })
    logger.error(message)
    return


class FilterNotPassed(Exception):
    """
    FilterNotPassed is raised when a tweet fails to pass one of the filters of the pipeline.
    This is not considered an error, but a normal behavior in the system.
    The exception is used to interrupt the subtask chain.
    """
    def __init__(self, msg, channel_id):
        self.msg = msg
        self.channel_id = channel_id
        channel_log_info.delay(msg, channel_id)


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

            if channel.scheduleblocks_enabled:
                eta = self.calculate_eta(tweet.type)
            else:
                eta = datetime.datetime.now()

            if eta is None:
                msg = "#%s marked as NOT SENT: No schedules for %s" % (tweet.tweet_id,
                                                                       tweet.get_type_display())
                channel_log_info.delay(msg, self.screen_name)
                tweet.status = Tweet.STATUS_NOT_SENT
                tweet.save()
            else:
                countdown = (eta - datetime.datetime.now()).total_seconds()
                retweet.s().apply_async(args=args, kwargs=kwargs, countdown=countdown)

                if countdown > 1:
                    msg = "#%s has been DELAYED until %s" % (tweet.tweet_id, eta)
                    channel_log_info.delay(msg, self.screen_name)

                return self.run(*args, **kwargs)    # Does nothing

    def set_channel_id(self, id):
        self.screen_name = id

    def calculate_eta(self, tweet_type):
        """ Given a tweet type, it calculates the seconds until an available schedule block is found """
        blocks = ChannelScheduleBlock.objects.filter(channel=self.screen_name)
        eta = datetime.datetime.max
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
        """ calls the subtask chain for mentions and DMs received by the stream """
        if 'text' in data:
            for mention in data['entities']['user_mentions']:
                if self.channel.screen_name.lower() == mention['screen_name'].lower():
                    (
                        store_tweet.s(data, self.channel.screen_name) |
                        triggers_filter.subtask() |
                        is_user_allowed.subtask() |
                        banned_words_filter.subtask() |
                        delay_retweet.subtask()
                    ).apply_async()

        elif 'direct_message' in data:
            (
                store_tweet.s(data, self.channel.screen_name) |
                triggers_filter.subtask() |
                is_user_allowed.subtask() |
                banned_words_filter.subtask() |
                delay_retweet.subtask()
            ).apply_async()

    def on_error(self, status_code, data):
        msg = "Error in streaming: %s: %s" % (status_code, data)
        channel_log_error.delay(msg, self.channel.screen_name)
        self.disconnect()
        self.channel.retweets_enabled = False
        self.channel.save()
        # should retry??

    def disconnect(self):
        """Used to disconnect the streaming client manually"""
        msg = "Disconnected stream client"
        channel_log_info.delay(msg, self.channel.screen_name)
        self.connected = False


@task(queue="streaming", ignore_result=True, default_retry_delay=60, max_retries=None)
def stream_channel(chan_id):
    """ This task initializes a channel streaming process, if it isn't active yet (uses cache lock to verify) """
    chan = Channel.objects.get(screen_name=chan_id)
    if cache.add("streaming_lock_%s" % chan.screen_name, "true", None):  # Acquire lock
        try:
            message = "Starting streaming for %s" % chan_id
            channel_log_info.delay(message, chan.screen_name)
            stream = ChannelStreamer(chan, current_task)
            stream.user(**{"with": "followings"})
            return True
        except Exception as e:
            cache.delete("streaming_lock_%s" % chan.screen_name)   # release lock
            message = "Error starting streaming for %s. Will retry later: %s" % (chan_id, e)
            channel_log_exception.delay(message, chan.screen_name)
            stream_channel.retry(exc=e, chan_id=chan_id)
            return False
    else:
        channel_log_warning.delay("Channel tried to start duplicate streaming process", chan.screen_name)


@task(queue="tweets", ignore_result=True)
def store_tweet(data, channel_id):
    """ Stores tweet in database, and creates a Tweet instance to be handled by all other tasks """
    import HTMLParser
    html = HTMLParser.HTMLParser()

    try:
        if 'direct_message' in data:
            # it's a DM
            data = data['direct_message']
            tweet = Tweet()
            tweet.screen_name = data['sender']['screen_name']
            tweet.text = html.unescape(data['text'])
            tweet.tweet_id = data['id']
            tweet.source = 'DM'
            tweet.mention_to = data['recipient_screen_name']
            tweet.type = Tweet.TYPE_DM
            #tweet.save()
            channel_log_info.delay(tweet.__unicode__(), channel_id)
        elif 'text' in data:
            for mention in data['entities']['user_mentions']:
                if channel_id.lower() == mention['screen_name'].lower():
                    # it's a channel mention
                    tweet = Tweet()
                    tweet.screen_name = data['user']['screen_name']
                    tweet.text = html.unescape(data['text'])
                    tweet.tweet_id = data['id']
                    tweet.source = data['source']
                    tweet.mention_to = channel_id
                    tweet.type = Tweet.TYPE_MENTION
                    #tweet.save()
                    channel_log_info.delay(tweet.__unicode__(), channel_id)
        else:
            return None

        if cache.get('%s_limit_waiting' % tweet.mention_to) is not None:
            tweet.status = Tweet.STATUS_NOT_SENT
            #tweet.save()
            msg = "#%s marked as NOT SENT (waiting for update limit to pass)" % tweet.tweet_id
            channel_log_info.delay(msg, tweet.mention_to)
            return None
        else:
            return tweet
    except Exception as e:
        channel_log_exception.delay("Unexpected error in store_tweet task\n%s", (channel_id,e))


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def triggers_filter(tweet):
    """ Checks if tweet has any trigger in it. If not, FilterNotPassed exception is raised """
    if tweet is not None:
        channel = Channel.objects.filter(screen_name=tweet.mention_to)[0]

        # if feature is disabled, pass the tweet
        if not channel.triggers_enabled:
            tweet.status = Tweet.STATUS_TRIGGERED
            return tweet

        triggers = channel.get_group_items("Trigger")

        try:
            for tr in triggers:
                if tr.occurs_in(tweet.strip_channel_mention()):
                    tweet.status = Tweet.STATUS_TRIGGERED
                    msg = "Marked #%s as TRIGGERED (found trigger '%s')" % (tweet.tweet_id, tr.text)
                    channel_log_info.delay(msg, channel.screen_name)
                    return tweet
            else:
                tweet.status = Tweet.STATUS_NOT_TRIGGERED
                #tweet.save()
                msg = "Marked #%s as NOT TRIGGERED" % tweet.tweet_id
                raise FilterNotPassed(msg, channel.screen_name)
        except FilterNotPassed:
            raise
        except:
            import sys
            channel_log_exception.delay("Unexpected error in triggers_filter task: %s" % sys.exc_info()[0], channel.screen_name)


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def is_user_allowed(tweet):
    """ Checks if user is blacklisted before retweeting """
    if tweet is not None:
        from_user = tweet.screen_name
        channel = Channel.objects.get(screen_name=tweet.mention_to)

        try:
            # if feature is disabled, pass the tweet
            if not channel.blacklist_enabled:
                return tweet

            blocked_users = channel.get_group_items("BlockedUser")
            for user in blocked_users:
                if user.screen_name.lower() == from_user.lower():
                    # user is blocked
                    tweet.status = Tweet.STATUS_BLOCKED
                    #tweet.save()
                    msg = "#%s marked as BLOCKED (user @%s is blacklisted)" % (tweet.tweet_id,
                                                                               user.screen_name)
                    raise FilterNotPassed(msg, channel.screen_name)
            else:
                return tweet
        except FilterNotPassed as exc:
            raise
        except:
            import sys
            channel_log_exception.delay("Unexpected error in is_user_allowed task: %s" % sys.exc_info()[0],
                channel.screen_name)


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def banned_words_filter(tweet):
    """ Checks if there's any banned word in tweet content. If so, FilterNotPassed exception is raised """
    if tweet is not None and tweet.status == Tweet.STATUS_TRIGGERED:
        channel = Channel.objects.filter(screen_name=tweet.mention_to)[0]
        
        # if feature is disabled, pass the tweet
        if not channel.filters_enabled:
            tweet.status = Tweet.STATUS_APPROVED
            return tweet

        filters = channel.get_group_items("Filter")
        try:
            for filter in filters:
                if filter.occurs_in(tweet.strip_channel_mention()):
                    tweet.status = Tweet.STATUS_BLOCKED
                    #tweet.save()
                    msg = "#%s marked as BLOCKED (found word '%s')" % (tweet.tweet_id, filter.text)
                    raise FilterNotPassed(msg, channel.screen_name)
            else:
                tweet.status = Tweet.STATUS_APPROVED
                return tweet
        except FilterNotPassed as exc:
            raise
        except:
            import sys
            channel_log_exception.delay("Unexpected error in banned_words_filter task: %s" % sys.exc_info()[0],
                channel.screen_name)


@task(queue="tweets", base=RetweetDelayedTask, ignore_result=True, expires=TASK_EXPIRES)
def delay_retweet(tweet):
    """ Delays tweet until next available schedule. Responsible code is in RetweetDelayedTask class """
    pass


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def retweet(tweet, txt=None, applying_hashtag=None):
    """ 
    If tweet is approved, applies replacements and hashtags. Then it schedules tweeting DELAY_DELTA seconds 
    after last tweet. This is to prevent update limit events
    """
    LOCK_EXPIRE = 60 * 5    # Lock expires in 5 minutes
    DELAY_DELTA = 90        # allows updating status each minute per channel

    if tweet is not None and tweet.status == Tweet.STATUS_APPROVED:
        channel = Channel.objects.get(screen_name=tweet.mention_to)

        if not channel.prevent_update_limit:
            DELAY_DELTA = 0
            
        if txt is None:
            txt = tweet.strip_channel_mention()

            # Apply replacements
            if channel.replacements_enabled:
                reps = channel.get_group_items("Replacement")

                for rep in reps:
                    txt = rep.replace_in(txt)

            txt = "via @%s: %s" % (tweet.screen_name, txt)

            # Apply hashtags
            if channel.hashtags_enabled and applying_hashtag is None:
                hashtag_list = []
                hashtags = channel.get_group_items("Hashtag")
                
                for hashtag in hashtags:
                    if hashtag.status == 1 and hashtag.applies_now() and len(hashtag.text) + 1 <= (140 - len(txt)) \
                    and hashtag.is_under_daily_limit():
                        hashtag_list.append(hashtag)
                
                if hashtag_list:
                    applying_hashtag = hashtag_list[randint(0, len(hashtag_list) - 1)]
                    txt = "%s %s" % (txt, applying_hashtag.text)

        # acquire lock
        if cache.add("retweet_lock_%s" % channel.screen_name, "true", LOCK_EXPIRE):
            try:
                last = cache.get('%s_last_tweet' % channel.screen_name)
                now = datetime.datetime.now()

                if last is not None and (now - last).total_seconds() < DELAY_DELTA:
                    # if it's not first tweet and last tweet is recent, delay.
                    eta = last + datetime.timedelta(seconds=DELAY_DELTA)
                    countdown = (eta - now).total_seconds()
                    if countdown < TASK_EXPIRES:
                        cache.set('%s_last_tweet' % channel.screen_name, eta)
                        update_status.s().apply_async(args=[channel.screen_name, tweet, txt, applying_hashtag],
                            countdown=countdown)
                        msg = "#%s will be sent in %s seconds" % (tweet.tweet_id, countdown)
                        channel_log_info.delay(msg, channel.screen_name)
                    else:
                        tweet.status = Tweet.STATUS_NOT_SENT
                        #tweet.save()
                        msg = "#%s marked as NOT SENT (Too many messages in queue)" % tweet.tweet_id
                        channel_log_info.delay(msg, channel.screen_name)
                else:
                    # send now
                    update_status.s().apply_async(args=[channel.screen_name, tweet, txt, applying_hashtag],
                        countdown=0)
                    cache.set('%s_last_tweet' % channel.screen_name, now)   # update locked eta
            finally:
                cache.delete("retweet_lock_%s" % channel.screen_name)    # release lock
        else:
            retweet.apply_async(args=[tweet, txt, applying_hashtag], countdown=5)
            # channel eta lock is busy, retry 5 seconds later
    return tweet


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES, max_retries=3)
def update_status(channel_id, tweet, txt, hashtag=None):
    """ sends processed tweet to the timeline """
    channel = Channel.objects.get(screen_name=channel_id)
    try:
        update_limit = cache.get('%s_limit_waiting' % channel.screen_name)
        if channel.retweets_enabled and update_limit is None:
            api = ChannelAPI(channel)
            if len(txt) > 140:
                txt = txt[0:139]
            api.tweet(txt)

            tweet.status = Tweet.STATUS_SENT
            tweet.retweeted_text = txt
            tweet.save()

            cache.delete('%s_limit_count' % channel.screen_name)
            msg = "Retweeted #%s succesfully and marked it as SENT" % tweet.tweet_id
            channel_log_info.delay(msg, channel.screen_name)
        else:
            tweet.status = Tweet.STATUS_NOT_SENT
            tweet.retweeted_text = txt
            #tweet.save()

            reason = "channel was disabled" if update_limit is None else "update limit: waiting %s seconds" % update_limit
            msg = "#%s marked as NOT SENT (%s)" % (tweet.tweet_id, reason)
            channel_log_info.delay(msg, channel.screen_name)

    except Exception, e:
        if "update limit" in e.args[0]:
            HOLD_ON_WINDOW = 300   # 5 minutes

            count = cache.get('%s_limit_count' % channel.screen_name)
            if count is None:
                count = 1
            else:
                count += 1

            seconds_waiting = HOLD_ON_WINDOW * count
            cache.set('%s_limit_count' % channel.screen_name, count, seconds_waiting * 2)
            cache.set('%s_limit_waiting' % channel.screen_name, seconds_waiting, seconds_waiting)

            limit = UpdateLimit.create(channel, seconds_waiting)
            channel_log_warning.delay(limit, channel.screen_name)
        elif "duplicate" in e.args[0]:
            pass
        elif "over 140" in e.args[0]:
            pass
        else:
            # unknown error ocurred, retry later
            if update_status.request.retries < 3:
                channel_log_exception.delay(
                    "Couldn't send #%s, retrying later (%s retries so far)" % (tweet.tweet_id,
                                                                               update_status.request.retries),
                    channel.screen_name)
                raise update_status.retry(exc=e)
            else:
                pass

        tweet.status = Tweet.STATUS_NOT_SENT
        tweet.save()
        msg = "#%s marked as NOT SENT: %s" % (tweet.tweet_id, e)
        channel_log_exception.delay(msg, channel.screen_name)
    else:
        # if no exception was raised and hashtag was included, increase count.
        if hashtag:
            appliance = HashtagAppliance(hashtag=hashtag, channel=channel)
            appliance.save()


@worker_init.connect
def worker_init_handler(sender=None, **kwargs):
    """ initializes all streaming processes when streaming worker starts """
    if "streaming" in sender.app.amqp.queues:
        print "Streaming worker initialized."
        channels = Channel.objects.all()
        for chan in channels:
            if chan.retweets_enabled:
                chan.init_streaming(force=True)
            else:
                chan.stop_streaming()


@worker_shutdown.connect
def worker_shutdown_handler(sender=None, **kwargs):
    """ releases all streaming locks before shutting down """
    if "streaming" in sender.app.amqp.queues:
        print "Streaming worker shutting down..."
        channels = Channel.objects.all()
        for chan in channels:
            chan.stop_streaming()
            cache.delete("streaming_lock_%s" % chan.screen_name)
