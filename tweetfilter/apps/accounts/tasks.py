# -*- coding: utf-8 -*-


import datetime
import re
from exceptions import Exception
from celery import task
from celery._state import current_task
from apps.accounts.backends import ChannelStreamer
from apps.accounts.models import ChannelScheduleBlock, Channel
from apps.control.tasks import DelayedTask
from apps.filtering.models import BlockedUser
from apps.twitter.api import ChannelAPI
from apps.twitter.models import Tweet

from unidecode import unidecode


class RetweetDelayedTask(DelayedTask):
    """
    DelayedTask class for the automatic retweet task.
    It should only run if now() is inside any of the account's timeblocks.
    It should delay execution until next available datetime otherwise.
    """
    screen_name = ""
    max_retries = 0     # I don't like this

    def __call__(self, *args, **kwargs):
        self.screen_name = kwargs['screen_name']
        tweet = args[0]     # Tweet object

        if tweet.status == Tweet.STATUS_APPROVED:
            # calculate nearest ETA and delay itself until then
            eta = self.calculate_eta()
            print "Retweet task %s will execute on %s" % (current_task.request.id, eta)
            #print "now is %s" % datetime.datetime.now()
            #print "task name = %s" % current_task.name
            """try:
                current_task.retry(args=args, kwargs=kwargs, eta=eta)
            except Exception:
                pass    # all cool"""
            retweet.s().apply_async(args=args, kwargs=kwargs, eta=eta)
            return self.run(*args, **kwargs)
        else:
            pass    # nothing happens, tweet shouldn't be retweeted

    def set_channel_id(self, id):
        self.screen_name = id

    def can_execute_now(self):
        blocks = ChannelScheduleBlock.objects.filter(channel=self.screen_name)
        if len(blocks) > 0:
            result = False
        else:
            result = True

        now = datetime.datetime.now()
        for block in blocks:
            if block.has_datetime(now):
                result = True

        if result:
            print "can execute"
        else:
            print "can't execute now"

        return result

    def calculate_eta(self):
        blocks = ChannelScheduleBlock.objects.filter(channel=self.screen_name)
        if len(blocks) > 0:
            eta = blocks[0].next_datetime()
        else:
            eta = datetime.datetime.now()

        for block in blocks:
            block_eta = block.next_datetime()
            if block_eta < eta:
                eta = block_eta
        return eta


@task(queue="streaming")
def stream_channel(chan_id):
    print "Starting streaming for channel %s" % chan_id
    try:
        chan = Channel.objects.filter(screen_name=chan_id)[0]
        stream = ChannelStreamer(chan)
        stream.user(**{"with": "followings"})
        return True
    except Exception as e:
        print "Error al iniciar streaming: %s" % e
        return False


@task(queue="tweets")
def triggers_filter(tweet, channel):
    if tweet.status is not Tweet.STATUS_BLOCKED:
        triggers = channel.get_triggers()
        try:
            for tr in triggers:

                word = unidecode(tr.text.lower())  # hace match con la palabra rodeada de espacios
                if word in unidecode(tweet.text.lower()):

                    tweet.status = Tweet.STATUS_TRIGGERED
                    tweet.save()
                    print "Marked #%s as TRIGGERED (found the trigger '%s')" % (tweet.tweet_id, word)
                    break
            else:
                print "Marked #%s as NOT TRIGGERED" % tweet.tweet_id
                tweet.status = Tweet.STATUS_NOT_TRIGGERED
                tweet.save()
        except Exception, e:
            print "error en trigger update: %s" % e

    return tweet



@task(queue="tweets")
def banned_words_filter(tweet, channel):
    from unidecode import unidecode
    filters = channel.get_filters()
    if tweet is not None and tweet.status == Tweet.STATUS_TRIGGERED:
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
        is_user_allowed.s(channel=chan) |
        triggers_filter.s(channel=chan) |
        banned_words_filter.s(channel=chan) |
        delay_retweet.s(screen_name=chan.screen_name)).apply_async()
    return res

@task(queue="tweets")
def filter_pipeline_dm(data, chan):
    from apps.twitter import tasks
    res =(
        tasks.store_dm.s(data) |
        is_user_allowed.s(channel=chan) |
        triggers_filter.s(channel=chan) |
        banned_words_filter.s(channel=chan) |
        delay_retweet.s(channel=chan)).apply_async()  #delayed
    return res

@task(queue="tweets")
def is_user_allowed(tweet, channel):
    from_user = tweet.screen_name
    blocked_users = BlockedUser.objects.filter(channel=channel)
    for user in blocked_users:
        if user.screen_name.lower() == from_user.lower():
            # user is blocked
            tweet.status = Tweet.STATUS_BLOCKED
            tweet.save()
            print "Tweet %s marked as BLOCKED (sent from blacklisted user @%s)" % (tweet.tweet_id, user.screen_name)
    return tweet

@task(queue="tweets", base=RetweetDelayedTask)
def delay_retweet(tweet, screen_name):
    pass


@task(queue="tweets")
def retweet(tweet, screen_name):
    channel = Channel.objects.get(screen_name=screen_name)
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

