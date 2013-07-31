from django.db import models

# Create your models here.
from apps.channels.models import Channel


class Trigger(models.Model):
    ACTION_RETWEET = 1

    ACTION_CHOICES = (
        (ACTION_RETWEET, "Retweet"),
    )

    text = models.CharField(max_length=32)
    action = models.IntegerField(choices=ACTION_CHOICES, default=ACTION_RETWEET)
    channel = models.ForeignKey(Channel)
    enabled_mentions = models.BooleanField(default=True)
    enabled_dm = models.BooleanField(default=True)


class Filter(models.Model):
    ACTION_BLOCK_TWEET = 1
    ACTION_BLOCK_USER = 2

    ACTION_CHOICES = (
        (ACTION_BLOCK_TWEET, "Bloquear tweet"),
        (ACTION_BLOCK_USER, "Bloquear usuario"),
        )

    text = models.CharField(max_length=32)
    action = models.SmallIntegerField(choices=ACTION_CHOICES, default=ACTION_BLOCK_TWEET)
    channel = models.ForeignKey(Channel)
    enabled_mentions = models.BooleanField(default=True)
    enabled_dm = models.BooleanField(default=True)

# Lista "negra"
class BlockedUser(models.Model):
    screen_name = models.CharField(max_length=16)
    block_date = models.DateTimeField(auto_now=True)
    block_duration = models.IntegerField()
    reason = models.CharField(max_length=64)
    channel = models.ForeignKey(Channel)

# Lista "blanca"
class AllowedUser(models.Model):
    screen_name = models.CharField(max_length=16)
    channel = models.ForeignKey(Channel)