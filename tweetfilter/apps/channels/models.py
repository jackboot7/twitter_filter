from celery.worker.control import Panel
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
import django.db.models
from apps.twitter.models import Tweet


class Channel(models.Model):
    DISABLED_STATUS = 0
    ENABLED_STATUS = 1

    STATUS_CHOICES = (
        (DISABLED_STATUS, 'Inactivo'),
        (ENABLED_STATUS, 'Activo')
    )

    screen_name = models.CharField(max_length=16, unique=True, primary_key=True)
    oauth_token = models.CharField(max_length=128)
    oauth_secret = models.CharField(max_length=128)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=ENABLED_STATUS)
    user = models.ForeignKey(User, blank=True, null=True)
    streaming_task_id = models.CharField(max_length=64)

    def get_last_update(self):
        try:
            update = Tweet.objects.filter(status=Tweet.SENT_STATUS, mention_to=self.screen_name).order_by('-id')[0]
            return update
        except Exception, e:
            return None

    def activate(self):
        self.status = self.ENABLED_STATUS
        self.save()
        self.init_streaming()

    def deactivate(self):
        self.status = self.DISABLED_STATUS
        self.save()
        self.stop_streaming()

    def is_active(self):
        return self.status == self.ENABLED_STATUS

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

    def init_streaming(self):
        from apps.twitter.tasks import stream_channel
        task = stream_channel.delay(self)
        self.streaming_task_id = task.id
        self.save()

    def stop_streaming(self):
        from celery.worker.control import revoke
        revoke(panel=Panel(), task_id=self.streaming_task_id, terminate=True)