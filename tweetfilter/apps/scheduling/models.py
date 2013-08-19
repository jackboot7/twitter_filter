from celery.schedules import crontab
from django.db import models
from djcelery.models import PeriodicTask, CrontabSchedule
from apps.accounts.models import Channel
from apps.control.models import Schedule

class ScheduledTweet(Schedule):
    STATUS_DISABLED = 0
    STATUS_ENABLED = 1

    STATUS_CHOICES = (
        (STATUS_DISABLED, "Desactivado"),
        (STATUS_ENABLED, "Activado")
    )

    text = models.CharField(max_length=140)
    channel = models.ForeignKey(Channel)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ENABLED)

    def save(self, *args, **kwargs):
        super(ScheduledTweet, self).save(*args, **kwargs)

        print "saving %s" % self.channel.screen_name
        for count, thing in enumerate(args):
            print '{0}. {1}'.format(count, thing)
        for name, value in kwargs.items():
            print '{0} = {1}'.format(name, value)

        PeriodicTask(
            name="%s-schedule-%s"%(self.channel.screen_name, self.id),
            task=u"apps.scheduling.tasks.schedule_tweet",
            crontab=CrontabSchedule(
                minute=self.time.minute,
                hour=self.time.hour,
                day_of_week=self.days_of_week_string()),

            #interval=IntervalSchedule.objects.get_or_create(every=10,period=u'seconds')[0],
            args=[self.channel.screen_name]
        ).save()

    def get_excerpt(self):
        max_chars = 32
        return self.text[0:max_chars]