# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from picklefield.fields import PickledObjectField
from apps.control.models import ScheduleBlock
from apps.twitter.models import Tweet


class Channel(models.Model):
    STATUS_DISABLED = 0
    STATUS_ENABLED = 1

    STATUS_CHOICES = (
        (STATUS_DISABLED, 'Inactivo'),
        (STATUS_ENABLED, 'Activo')
    )

    ALLOW_ALL = 0
    ALLOW_FOLLOWERS_ONLY = 1

    ALLOW_CHOICES = (
        (ALLOW_ALL, "Todos los usuarios"),
        (ALLOW_FOLLOWERS_ONLY, "Sólo seguidores")
    )

    screen_name = models.CharField(max_length=16, unique=True, primary_key=True)
    oauth_token = models.CharField(max_length=128)
    oauth_secret = models.CharField(max_length=128)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ENABLED)
    user = models.ForeignKey(User, blank=True, null=True)

    # Resultado de la tarea de streaming (necesario para desactivar)
    streaming_task = PickledObjectField()

    # indica si hace retweet de mentions y/o DMs
    enabled_mentions = models.BooleanField(default=True)
    enabled_dm = models.BooleanField(default=True)

    # indica quiénes pueden enviar mensajes al canal
    allow_messages = models.SmallIntegerField(choices=ALLOW_CHOICES, default=ALLOW_ALL)


    def get_last_update(self):
        try:
            update = Tweet.objects.filter(status=Tweet.STATUS_SENT, mention_to=self.screen_name).order_by('-id')[0]
            return update
        except Exception, e:
            return None

    def activate(self):
        self.status = self.STATUS_ENABLED
        self.save()
        #self.init_streaming()

    def deactivate(self):
        self.status = self.STATUS_DISABLED
        self.save()
        #self.stop_streaming()

    def is_active(self):
        return self.status == self.STATUS_ENABLED

    def switch_status(self):
        try:
            if self.is_active():
                self.deactivate()
            else:
                self.activate()
            return True
        except Exception, e:
            print e
            return False

    """
    def init_streaming(self):
        task = stream_channel.delay(self)
        self.streaming_task = task
        print "Initializing task id = %s (%s)" % (task.id, self.screen_name)
        self.save()
    """

    """
    def stop_streaming(self):
        try:
            self.streaming_task.revoke(terminate=True)
        except Exception, e:
            print "streaming task doesn't exist yet (%s)" % e
    """
    """
    # pendiente por implementar
    def is_streaming(self):
        task = self.streaming_task
        print "is %s streaming? %s" % (self.screen_name, task.state)

        return task.state == "PENDING" or \
               task.state == "STARTED" or \
               task.state == "RETRY"
    """


    def get_triggers(self):
        """
        Returns a list of this channel's trigger words
        """
        triggers = Trigger.objects.filter(channel=self)
        return triggers
        #return self.trigger_set.all()

    def get_filters(self):
        """
        Returns a list of this channel's trigger words
        """
        filters = Filter.objects.filter(channel=self)
        return filters
        #return self.filter_set.all()


class ChannelScheduleBlock(ScheduleBlock):
    channel = models.ForeignKey(Channel)


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

