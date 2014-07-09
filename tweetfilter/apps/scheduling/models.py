import json
from django.db import models
from djcelery.models import PeriodicTask, CrontabSchedule
from apps.accounts.models import Channel
from apps.control.models import Schedule, ItemGroup


class ScheduledTweet(Schedule):
    STATUS_DISABLED = 0
    STATUS_ENABLED = 1

    STATUS_CHOICES = (
        (STATUS_DISABLED, "Desactivado"),
        (STATUS_ENABLED, "Activado")
    )

    text = models.CharField(max_length=140)
    group = models.ForeignKey(ItemGroup, null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ENABLED)
    periodic_task = models.ForeignKey(PeriodicTask, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(ScheduledTweet, self).save(*args, **kwargs)

        # creates new periodic task
        if self.periodic_task is None:
            cron = CrontabSchedule(
                minute=self.time.minute,
                hour=self.time.hour,
                day_of_week=self.days_of_week_string())
            cron.save()

            ptask = PeriodicTask(
                name="%s-schedule-%s-%s"%(self.group.id, self.id, cron.id),
                task="apps.scheduling.tasks.schedule_tweet",
                crontab=cron,
                queue="scheduling",
                kwargs=json.dumps({'group_id': self.group.id,
                                   'text': self.text}))
            ptask.save()
            self.periodic_task = ptask
            super(ScheduledTweet, self).save(*args, **kwargs)
        else:
            ptask = self.periodic_task
            ptask.kwargs=json.dumps({'group_id': self.group.id,
                                     'text': self.text})
            cron = ptask.crontab
            cron.hour = self.time.hour
            cron.minute = self.time.minute
            cron.day_of_week = self.days_of_week_string()
            cron.save()
            ptask.save()

    def delete(self):
        ptask = self.periodic_task
        cron = ptask.crontab
        cron.delete()
        ptask.delete()        

    def get_excerpt(self):
        max_chars = 32
        return self.text[0:max_chars]