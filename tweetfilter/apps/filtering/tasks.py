# -*- coding: utf-8 -*-

import datetime
import logging
from random import randint

import gevent
from celery._state import current_task
from celery import task

from exceptions import Exception

from django.conf import settings
from django.core.cache import cache
from twython.streaming.api import TwythonStreamer

from apps.accounts.models import Channel
from apps.control.models import UpdateLimit
from apps.control.tasks import DelayedTask
from apps.filtering.models import BlockedUser, ChannelScheduleBlock, Replacement
from apps.hashtags.models import HashtagAdvertisement
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
        gevent.sleep(0)
        self.handle_data(data)

    def handle_data(self, data):
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


@task(queue="streaming", ignore_result=True, default_retry_delay=60, max_retries=10)
def stream_channel(chan_id):
    chan = Channel.objects.filter(screen_name=chan_id)[0]

    try:
        message = "Starting streaming for %s" % chan_id
        channel_log_info.delay(message, chan.screen_name)
        stream = ChannelStreamer(chan, current_task)
        stream.user(**{"with": "followings"})
        return True
    except Exception as e:
        message = u"Error starting streaming for %s. Will retry later: %s" % (chan_id, e)
        channel_log_exception.delay(message, chan.screen_name)
        stream_channel.retry(exc=e, chan_id=chan_id)
        return False


@task(queue="tweets", ignore_result=True)
def store_tweet(data, channel_id):
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
            tweet.save()
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
                    tweet.save()
                    channel_log_info.delay(tweet.__unicode__(), channel_id)
        else:
            # should we handle the rest of the tweets?
            # Maybe store them for future use.
            return None
        if cache.get('%s_limit_waiting' % tweet.mention_to) is not None:
            tweet.status = Tweet.STATUS_NOT_SENT
            tweet.save()
            msg = "#%s marked as NOT SENT (waiting for update limit to pass)" % tweet.tweet_id
            channel_log_info.delay(msg, tweet.mention_to)
            return None
        else:
            return tweet
    except Exception as e:
        channel_log_exception.delay("Unexpected error in store_tweet task\n%s", (channel_id,e))


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def triggers_filter(tweet):
    if tweet is not None:
        channel = Channel.objects.filter(screen_name=tweet.mention_to)[0]

        # if feature is disabled, pass the tweet
        if not channel.triggers_enabled:
            tweet.status = Tweet.STATUS_TRIGGERED
            return tweet

        triggers = channel.get_triggers()
        try:
            for tr in triggers:
                if tr.occurs_in(tweet.strip_channel_mention()):
                    tweet.status = Tweet.STATUS_TRIGGERED
                    msg = "Marked #%s as TRIGGERED (found trigger '%s')" % (tweet.tweet_id, tr.text)
                    channel_log_info.delay(msg, channel.screen_name)
                    return tweet
            else:
                tweet.status = Tweet.STATUS_NOT_TRIGGERED
                tweet.save()
                msg = "Marked #%s as NOT TRIGGERED" % tweet.tweet_id
                raise FilterNotPassed(msg, channel.screen_name)
        except FilterNotPassed:
            raise
        except:
            import sys
            channel_log_exception.delay("Unexpected error in triggers_filter task: %s" % sys.exc_info()[0], channel.screen_name)


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def is_user_allowed(tweet):
    if tweet is not None:
        from_user = tweet.screen_name
        channel = Channel.objects.get(screen_name=tweet.mention_to)

        try:
            # if feature is disabled, pass the tweet
            if not channel.blacklist_enabled:
                return tweet

            blocked_users = BlockedUser.objects.filter(channel=tweet.mention_to)
            for user in blocked_users:
                if user.screen_name.lower() == from_user.lower():
                    # user is blocked
                    tweet.status = Tweet.STATUS_BLOCKED
                    tweet.save()
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
    if tweet is not None and tweet.status == Tweet.STATUS_TRIGGERED:
        channel = Channel.objects.filter(screen_name=tweet.mention_to)[0]
        # if feature is disabled, pass the tweet
        if not channel.filters_enabled:
            tweet.status = Tweet.STATUS_APPROVED
            return tweet

        filters = channel.get_filters()
        try:
            for filter in filters:
                if filter.occurs_in(tweet.strip_channel_mention()):
                    tweet.status = Tweet.STATUS_BLOCKED
                    tweet.save()
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
    pass


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES)
def retweet(tweet, txt=None):
    LOCK_EXPIRE = 60 * 5    # Lock expires in 5 minutes
    DELAY_DELTA = 90        # allows updating status each minute per channel

    if tweet is not None and tweet.status == Tweet.STATUS_APPROVED:
        channel = Channel.objects.get(screen_name=tweet.mention_to)
        applying_hashtag = None

        if txt is None:
            txt = tweet.strip_channel_mention()

            # Apply replacements
            if channel.replacements_enabled:
                reps = Replacement.objects.filter(channel=tweet.mention_to)

                for rep in reps:
                    txt = rep.replace_in(txt)

            txt = "via @%s: %s" % (tweet.screen_name, txt)
            if len(txt) > 140:
                txt = txt[0:139]

            # Apply hashtags
            if channel.hashtags_enabled:
                hashtag_list = []
                hashtags = HashtagAdvertisement.objects.filter(channel=channel.screen_name)
                for hashtag in hashtags:
                    if hashtag.applies_now() and len(hashtag.text) + 1 <= 140 - len(txt) \
                    and hashtag.count < hashtag.quantity:
                        hashtag_list.append(hashtag)

                if len(hashtag_list) > 0:
                    applying_hashtag = hashtag_list[randint(0, len(hashtag_list) - 1)]
                    txt = "%s #%s" % (txt, applying_hashtag.text)
                    #applying_hashtag.count += 1
                    #applying_hashtag.save()
                    # registrar en el log?

        # acquire lock
        if cache.add("retweet_lock_%s" % channel.screen_name, "true", LOCK_EXPIRE):
            try:
                last = cache.get('%s_last_tweet' % channel.screen_name)
                now = datetime.datetime.now()
                #print "now = %s" % now     # correct

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
                        tweet.save()
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
            retweet.apply_async(args=[tweet, txt], countdown=5)
            # channel eta lock is busy, retry 5 seconds later
    return tweet


@task(queue="tweets", ignore_result=True, expires=TASK_EXPIRES, max_retries=3)
def update_status(channel_id, tweet, txt, hashtag=None):
    channel = Channel.objects.get(screen_name=channel_id)
    try:
        update_limit = cache.get('%s_limit_waiting' % channel.screen_name)
        if channel.retweets_enabled and update_limit is None:
            api = ChannelAPI(channel)
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
            tweet.save()
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
            cache.set('%s_limit_count' % channel.screen_name, count, HOLD_ON_WINDOW * 2)
            cache.set('%s_limit_waiting' % channel.screen_name, HOLD_ON_WINDOW * count, HOLD_ON_WINDOW * count)

            limit = UpdateLimit.create(channel)
            channel_log_warning.delay(limit, channel.screen_name)
        elif "duplicate" in e.args[0]:
            pass
        elif "over 140" in e.args[0]:
            pass
        else:
            # unknown error ocurred, retry later
            print "retries so far: %s" % update_status.request.retries
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
        if hashtag is not None:
            hashtag.count += 1
            hashtag.save()
