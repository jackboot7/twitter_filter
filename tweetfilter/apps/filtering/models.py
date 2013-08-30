import django.db.models
from unidecode import unidecode
from apps.accounts.models import Channel
from django.db import models

# Create your models here.
from apps.control.models import ScheduleBlock
from apps.twitter.models import Tweet

class BlockedUser(models.Model):
    screen_name = models.CharField(max_length=16)
    block_date = models.DateTimeField(auto_now=True)
    block_duration = models.IntegerField(null=True, blank=True)  #days
    reason = models.CharField(max_length=64, blank=True)
    channel = models.ForeignKey(Channel)


class AllowedUser(models.Model):
    screen_name = models.CharField(max_length=16)
    channel = models.ForeignKey(Channel)


class ChannelScheduleBlock(ScheduleBlock):
    channel = models.ForeignKey(Channel)
    allow_mentions = models.BooleanField(default=True)
    allow_dm = models.BooleanField(default=True)

    def allows(self, type):
        if type == Tweet.TYPE_MENTION:
            return self.allow_mentions
        if type == Tweet.TYPE_DM:
            return self.allow_dm


class Keyword(models.Model):
    text = models.CharField(max_length=32)

    def equals(self, other_text):
        return unidecode(self.text.lower()) == unidecode(other_text.lower())

    def occurs_in(self, string):
        # THIS NEEDS TO BE FIXED
        # string should be "parsed" (splitted in relationship to spaces and punctuation signs) and compare each _word_
        words = "".join((char if char.isalpha() else " ") for char in unidecode(string.lower())).split()
        return unidecode(self.text.lower()) in words


class Trigger(Keyword):
    ACTION_RETWEET = 1

    ACTION_CHOICES = (
        (ACTION_RETWEET, "Retweet"),
    )

    #text = models.CharField(max_length=32)
    action = models.IntegerField(choices=ACTION_CHOICES, default=ACTION_RETWEET)
    channel = models.ForeignKey(Channel)
    enabled_mentions = models.BooleanField(default=True)
    enabled_dm = models.BooleanField(default=True)


class Filter(Keyword):
    ACTION_BLOCK_TWEET = 1
    ACTION_BLOCK_USER = 2

    ACTION_CHOICES = (
        (ACTION_BLOCK_TWEET, "Bloquear tweet"),
        (ACTION_BLOCK_USER, "Bloquear usuario"),
        )

    #text = models.CharField(max_length=32)
    action = models.SmallIntegerField(choices=ACTION_CHOICES, default=ACTION_BLOCK_TWEET)
    channel = models.ForeignKey(Channel)
    enabled_mentions = models.BooleanField(default=True)
    enabled_dm = models.BooleanField(default=True)