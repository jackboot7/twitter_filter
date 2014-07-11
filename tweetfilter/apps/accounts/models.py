# -*- encoding: utf-8 -*-
from django.core.cache import cache
from django.contrib.auth.models import User
from django.db import models
from picklefield.fields import PickledObjectField
from django.contrib.contenttypes.models import ContentType

from apps.control.tasks import channel_is_streaming, queue_is_active, get_streaming_task_ids
from apps.twitter.models import Tweet


class ItemGroup(models.Model):
    """
    Serves as a wrapper for a set of items of the same type (triggers, hashtags, blocked users, etc).
    Its purpose is to integrate different channels so that they can share items, clearing the need to
    redefine settings for each channel. 
    """
    content_type = models.ForeignKey(ContentType)
    name = models.CharField(max_length=64)
    channel_exclusive = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        class_type = kwargs.pop('class_type', None)
        super(ItemGroup, self).__init__(*args, **kwargs)
        if class_type is not None:
            self.content_type = ContentType.objects.get_for_model(class_type)

    def get_class(self):
        return self.content_type.model_class()

    def get_channels(self):
        return self.channel_set.all()


class Channel(models.Model):
    """
    A Channel represents a twitter account that is subscribed to the app service 
    """
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

    #
    groups = models.ManyToManyField(ItemGroup)

    def delete(self):
        """ stops streaming and scheduled tasks before deleting itself """
        self.stop_streaming()
        schedules = self.scheduledtweet_set.all()
        for schedule in schedules:
            schedule.delete()
        super(Channel, self).delete()

    def get_last_update(self):
        """ gets channel's last succesfully sent tweet """
        try:
            update = Tweet.objects.filter(status=Tweet.STATUS_SENT, mention_to=self.screen_name).order_by('-id')[0]
            return update
        except Exception, e:
            return None

    def activate(self):
        """ sets status as enabled and initializes streaming task """
        self.status = self.STATUS_ENABLED
        if self.init_streaming():
            self.save()

    def deactivate(self):
        """ sets status as disabled and stops streaming task """
        self.status = self.STATUS_DISABLED

        if self.stop_streaming():
            self.save()

    def is_active(self):
        """ returns channel status """
        return self.status == self.STATUS_ENABLED

    def switch_status(self):
        """ changes channel status """
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
        """ returns True if its streaming task is currently active """
        return channel_is_streaming(self.screen_name, exclude_task_id)

    def init_streaming(self, force=False):
        """ initializes channel streaming task """
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
        """ revokes channel streaming task """
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
        """ returns a list of this channel's trigger words """
        return self.trigger_set.all()

    def get_filters(self):
        """ returns a list of this channel's filter words """
        return self.filter_set.all()

    def get_groups(self, clazz):
        """ returns a list of item groups of certain type """
        clazz_type = ContentType.objects.get_for_model(clazz)
        return self.groups.filter(content_type__pk=clazz_type.id)

    def init_default_groups(self):
        """ creates default item groups for the channel. This should be called only once after authentication """
        self.groups.add(
            ItemGroup(class_type=Trigger, channel_exclusive=True, name="Disparadores del canal"), 
            ItemGroup(class_type=Filter, channel_exclusive=True, name="Retenedores del canal"),
            ItemGroup(class_type=Replacement, channel_exclusive=True, name="Supresores del canal"),
            ItemGroup(class_type=BlockedUser, channel_exclusive=True, name="Usuarios bloqueados del canal"),
            ItemGroup(class_type=ScheduledTweet, channel_exclusive=True, name="Tweets programados del canal"),
            ItemGroup(class_type=HashtagAdvertisement, channel_exclusive=True, name="Sufijos del canal"))
        self.save()