from django.contrib.auth.models import User
from django.db import models
from picklefield.fields import PickledObjectField
from apps.channels.tasks import stream_channel
from apps.twitter.models import Tweet


class Channel(models.Model):
    STATUS_DISABLED = 0
    STATUS_ENABLED = 1

    STATUS_CHOICES = (
        (STATUS_DISABLED, 'Inactivo'),
        (STATUS_ENABLED, 'Activo')
    )

    screen_name = models.CharField(max_length=16, unique=True, primary_key=True)
    oauth_token = models.CharField(max_length=128)
    oauth_secret = models.CharField(max_length=128)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ENABLED)
    user = models.ForeignKey(User, blank=True, null=True)
    streaming_task = PickledObjectField()

    def get_last_update(self):
        try:
            update = Tweet.objects.filter(status=Tweet.STATUS_SENT, mention_to=self.screen_name).order_by('-id')[0]
            return update
        except Exception, e:
            return None

    def activate(self):
        self.status = self.STATUS_ENABLED
        self.save()
        self.init_streaming()

    def deactivate(self):
        self.status = self.STATUS_DISABLED
        self.save()
        self.stop_streaming()

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

    def init_streaming(self):
        task = stream_channel.delay(self)
        #self.streaming_task_id = task.id
        self.streaming_task = task
        print "Initializing task id = %s (%s)" % (task.id, self.screen_name)
        self.save()

    def stop_streaming(self):
        #from celery.worker.control import revoke
        try:
            self.streaming_task.revoke(terminate=True)
        except Exception, e:
            print "streaming task doesn't exist yet (%s)" % e
        #revoke(panel=Panel(), task_id=self.streaming_task_id, terminate=True, signal='SIGTERM') #SIGKILL

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
        from apps.filtering.models import Trigger
        triggers = Trigger.objects.filter(channel=self)
        return triggers
        #return self.trigger_set.all()

    def get_filters(self):
        """
        Returns a list of this channel's trigger words
        """
        from apps.filtering.models import Filter
        filters = Filter.objects.filter(channel=self)
        return filters
        #return self.trigger_set.all()