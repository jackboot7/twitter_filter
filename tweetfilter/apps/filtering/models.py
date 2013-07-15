from django.db import models

# Create your models here.
from apps.channels.models import Channel

class Trigger(models.Model):
    RETWEET = 1

    ACTION_CHOICES = (
        (RETWEET, "Retweet"),
    )

    text = models.CharField(max_length=32)
    action = models.IntegerField(choices=ACTION_CHOICES)
    channel = models.ForeignKey(Channel)