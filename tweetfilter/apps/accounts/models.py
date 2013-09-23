# -*- encoding: utf-8 -*-
import os
import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from picklefield.fields import PickledObjectField
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

    # indica quiénes pueden enviar mensajes al canal
    allow_messages = models.SmallIntegerField(choices=ALLOW_CHOICES, default=ALLOW_ALL)

    logger = None   # Stores de logger object related to this channel

    def save(self, *args, **kwargs):
        super(Channel, self).save(*args, **kwargs)
        try:
            if self.filteringconfig is not None:
                pass
        except ObjectDoesNotExist:
            # if models is being saved for the first time,
            # instantiate FilteringConfig and SchedulingConfig
            filtering_config = FilteringConfig(channel=self)
            filtering_config.save()
            scheduling_config = SchedulingConfig(channel=self)
            scheduling_config.save()

    def delete(self):
        schedules = self.scheduledtweet_set.all()
        for schedule in schedules:
            schedule.delete()
        super(Channel, self).delete()

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

    def get_logger(self):
        from django.conf import settings
        if self.logger is None:
            handler = logging.handlers.RotatingFileHandler(
                filename=os.path.join(settings.LOGGING_ROOT, "%s.log" % self.screen_name),
                maxBytes=1024 * 1024 * 5,
                backupCount=5)

            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s %(name)-12s %(levelname)-8s %(message)s', '%a, %Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)

            self.logger = logging.getLogger("twitter.channels")   # fail?
            self.logger.handlers = []
            self.logger.addHandler(handler)

        return self.logger

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
        #triggers = Trigger.objects.filter(channel=self)
        #return triggers
        return self.trigger_set.all()

    def get_filters(self):
        """
        Returns a list of this channel's trigger words
        """
        #filters = Filter.objects.filter(channel=self)
        #return filters
        return self.filter_set.all()


class FilteringConfig(models.Model):
    channel = models.OneToOneField(Channel, parent_link=True)
    retweets_enabled = models.BooleanField(default=True)
    retweet_mentions = models.BooleanField(default=True)
    retweet_dm = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        channel = kwargs.pop('channel', None)
        super(FilteringConfig, self).__init__(*args, **kwargs)
        if channel is not None:
            self.channel = channel
            self.save()


class SchedulingConfig(models.Model):
    channel = models.OneToOneField(Channel, parent_link=True)
    scheduling_enabled = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        channel = kwargs.pop('channel', None)
        super(SchedulingConfig, self).__init__(*args, **kwargs)
        if channel is not None:
            self.channel = channel
            self.save()
