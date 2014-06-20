# -*- encoding: utf-8 -*-
from django.core.cache import cache
from django.contrib.auth.models import User
from django.db import models
from picklefield.fields import PickledObjectField
from apps.control.tasks import channel_is_streaming, queue_is_active, get_streaming_task_ids
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

    # tiempo máximo que debe esperarse antes de volver a enviar status
    # tweet_timedelta = models.IntegerField(default=60)

    # Resultado de la tarea de streaming (necesario para desactivar)
    streaming_task = PickledObjectField()

    # indica quiénes pueden enviar mensajes al canal
    allow_messages = models.SmallIntegerField(choices=ALLOW_CHOICES, default=ALLOW_ALL)

    # Filtering config
    retweets_enabled = models.BooleanField(default=False)
    retweet_mentions = models.BooleanField(default=True)
    retweet_dm = models.BooleanField(default=True)  # is module enabled
    triggers_enabled = models.BooleanField(default=True)
    replacements_enabled = models.BooleanField(default=True)
    filters_enabled = models.BooleanField(default=True)
    scheduleblocks_enabled = models.BooleanField(default=True)
    blacklist_enabled = models.BooleanField(default=True)
    prevent_update_limit = models.BooleanField(default=True)

    # Scheduling config
    scheduling_enabled = models.BooleanField(default=False)

    # Hashtags config
    hashtags_enabled = models.BooleanField(default=False)

    def delete(self):
        self.stop_streaming()
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
        if self.init_streaming():
            self.save()

    def deactivate(self):
        self.status = self.STATUS_DISABLED

        if self.stop_streaming():
            self.save()

    def is_active(self):
        return self.status == self.STATUS_ENABLED

    def switch_status(self):
        from apps.filtering.tasks import channel_log_error
        try:
            if self.is_active():
                self.deactivate()
            else:
                self.activate()
            return True
        except Exception, e:
            channel_log_error.delay("Uknown error occurred while switching channel status: %s" % e,
                self.screen_name)
            return False

    def is_streaming(self, exclude_task_id=None):
        return channel_is_streaming(self.screen_name, exclude_task_id)

    def init_streaming(self, force=False):
        STREAMING_QUEUE_NAME = "streaming"

        from apps.filtering.tasks import stream_channel, channel_log_exception
        try:
            if force or queue_is_active(STREAMING_QUEUE_NAME):
                stream_channel.delay(self.screen_name)
            return True
        except Exception, e:
            channel_log_exception.delay("Error while trying to initialize streaming: %s" % e,
                self.screen_name)
            return False

    def stop_streaming(self):
        from apps.filtering.tasks import channel_log_info, channel_log_exception
        from celery import current_app as app
        try:
            task_ids = get_streaming_task_ids(self.screen_name)
            if task_ids:
                for id in task_ids:
                    app.control.revoke(id, terminate=True)
                message = "Stopped streaming for %s" % self.screen_name
                channel_log_info.delay(message, self.screen_name)

            cache.delete("streaming_lock_%s" % self.screen_name)    # release lock
            return True
        except Exception, e:
            message = "Error while trying to stop streaming for %s: %s" % (self.screen_name, e)
            channel_log_exception.delay(message, self.screen_name)
            return False

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

        return self.filter_set.all()