# -*- coding: utf-8 -*-


import datetime
import re
from exceptions import Exception
from celery import task
from celery._state import current_task
from apps.accounts.backends import ChannelStreamer
from apps.accounts.models import ChannelScheduleBlock, Channel
from apps.control.backends import DelayedTask
from apps.twitter.api import ChannelAPI
from apps.twitter.models import Tweet

from unidecode import unidecode


class RetweetDelayedTask(DelayedTask):
    """
    DelayedTask class for the automatic retweet task.
    It should only run if now() is inside any of the account's timeblocks.
    It should delay execution until next available datetime otherwise.
    """
    screen_name = ""    # How do I set this????

    def __call__(self, *args, **kwargs):
        self.screen_name = kwargs['screen_name']
        if self.can_execute_now():
            # if "now" is in any of the channel related timeblocks
            return self.run(*args, **kwargs)    # execute task
        else:
            # calculate nearest ETA and delay itself until then
            eta = self.calculate_eta()
            print "Retweet task %s DELAYED until %s" % (current_task.request.id, eta)
            current_task.retry(args=args, kwargs=kwargs, eta=eta)

    def set_channel_id(self, id):
        self.screen_name = id

    def can_execute_now(self):
        blocks = ChannelScheduleBlock.objects.filter(channel=self.screen_name)

        now = datetime.datetime.now()
        for block in blocks:
            if block.has_datetime(now):
                return True
                break
        else:
            return False

        return True # since there are no time restrictions

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
        retweet.s(screen_name=chan.screen_name)).apply_async()
    return res

@task(queue="tweets")
def filter_pipeline_dm(data, chan):
    from apps.twitter import tasks
    res =(
        tasks.store_dm.s(data) |
        triggers_filter.s(channel=chan) |
        banned_words_filter.s(channel=chan) |
        retweet.s(channel=chan)).apply_async()  #delayed
    return res

@task(queue="tweets", base=RetweetDelayedTask)
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

