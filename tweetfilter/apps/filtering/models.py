import django.db.models
from unidecode import unidecode
from apps.accounts.models import Channel
from django.db import models

# Create your models here.
from apps.control.models import ScheduleBlock
from apps.twitter.models import Tweet

class BlockedUser(models.Model):
    """
    Defines a (twitter) user that is not allowed to send messages to the channel.
    Or more specifically, an account that is automatically discarded for retweeting.
    """
    screen_name = models.CharField(max_length=16)
    block_date = models.DateTimeField(auto_now=True)
    block_duration = models.IntegerField(null=True, blank=True)  #days
    reason = models.CharField(max_length=64, blank=True)
    channel = models.ForeignKey(Channel)


# lista blanca
class AllowedUser(models.Model):
    screen_name = models.CharField(max_length=16)
    channel = models.ForeignKey(Channel)


class ChannelScheduleBlock(ScheduleBlock):
    """
    It defines a schedule block where automatic retweeting is allowed for a specific channel
    """
    channel = models.ForeignKey(Channel)
    allow_mentions = models.BooleanField(default=True)
    allow_dm = models.BooleanField(default=True)

    def allows(self, type):
        if type == Tweet.TYPE_MENTION:
            return self.allow_mentions
        if type == Tweet.TYPE_DM:
            return self.allow_dm


class Keyword(models.Model):
    """
    Represents any kind of keyword (trigger, filter, labels, etc).
    The Keyword class implements methods for (case insensitive and
    special-character insensitive) string comparison.
    """
    text = models.CharField(max_length=32)

    def equals(self, other_text):
        return unidecode(self.text.lower()) == unidecode(other_text.lower())

    def occurs_in(self, string):
        if len(self.text.split()) > 1:
            # if the keyword is a phrase, searches for direct occurrence in the string
            return unidecode(self.text.lower()) in unidecode(string.lower())
        else:
            # else: searches for individual word occurrence
            words = "".join((char if char.isalpha() else " ") for char in unidecode(string.lower())).split()
            return unidecode(self.text.lower()) in words


class Trigger(Keyword):
    """
    A trigger is a word that makes the tweet be marked as "relevant".
    Only tweets containing triggers are candidates for retweeting
    """
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
    """
    Represents a keyword that is "banned" from the channel.
    If self.text exist in the incoming messsage, it won't be re-posted.
    """
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


class Replacement(Keyword):
    """
    Represents a word that is going to be deleted from the original text
    or replaced with an equivalent expression
    """
    channel = models.ForeignKey(Channel)
    replace_with = models.CharField(max_length=32)
    #enable_mentions
    #enable_dm