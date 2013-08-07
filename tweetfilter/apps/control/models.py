# -*- coding: utf-8 -*-
from time import strptime

from celery.schedules import crontab
from celery.task.base import PeriodicTask, Task
import datetime
from django.db import models


class TimeBlock(models.Model):
    start = models.TimeField()
    end = models.TimeField()

    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    def days_of_week_list(self):
        res = []
        if self.sunday:
            res.append(0)
        if self.monday:
            res.append(1)
        if self.tuesday:
            res.append(2)
        if self.wednesday:
            res.append(3)
        if self.thursday:
            res.append(4)
        if self.friday:
            res.append(5)
        if self.saturday:
            res.append(6)

        return res

    def has_day(self, day):
        print "type(day) = %s" % type(day)
        return day in self.days_of_week_list()

    def has_date_time(self, date_time):
        # ERROR de tipos en la conversión de str a time()
        start = strptime(self.start, "%H:%M")
        end = strptime(self.end, "%H:%M")
        return self.has_day(date_time.weekday()) and start <= date_time.time() < end

"""
class OneTimeTask(Task):
    start_time = models.DateTimeField()
    rate_limit = ""

#    def __init__(self):
#        super(OneTimeTask, self).__init__()
#        self.track_started = True   # useful for streaming tasks (initializes as started instead of pending)

    def __call__(self, *args, **kwargs):
        # calculate eta to start_stime, self.delay(eta)
        return self.run(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        #exit point
        pass


class RepeatTask(PeriodicTask):
    timeblock = TimeBlock()

    def __init__(self):
        #super(RepeatTask, self).__init__()
        self.run_every = crontab(
            hour=self.timeblock.start.hour,
            minute=self.timeblock.start.minute,
            day_of_week=self.timeblock.days_of_week_list())

    def __call__(self, *args, **kwargs):
        # add schedule with crontab !!!

        return self.run(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass
"""



"""
class ApplicationTask(models.Model):    # models.Model???
    TYPE_CONTINUOUS = 1
    TYPE_ONCE = 2
    TYPE_PERIODIC = 3
    TYPE_INTERVAL = 4

    TYPE_CHOICES = (
        (TYPE_CONTINUOUS, "Continua"),
        (TYPE_ONCE, "Una vez"),
        (TYPE_PERIODIC, "Periódica"),
        (TYPE_INTERVAL, "Intervalo")
    )

    STATUS_PENDING = 1
    STATUS_STARTED = 2
    STATUS_SUCCESS = 3
    STATUS_ERROR = 4

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pendiente"),
        (STATUS_STARTED, "Iniciada"),
        (STATUS_SUCCESS, "Exitosa"),
        (STATUS_ERROR, "Error")
    )

    celery_task = models.ForeignKey(Task)
    schedule = models.ForeignKey(Schedule)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=TYPE_ONCE)

    def __unicode__(self):
        self.celery_task.id

    def __init__(self, type, task, schedule):
        #super(ApplicationTask, self).__init__()
        self.celery_task = task
        self.type = type
        self.status = self.STATUS_PENDING
        self.schedule = schedule
        #self.calculate_schedule()

        if self.type == self.TYPE_CONTINUOUS:
            self.celery_task.track_started = True

        self.save()

"""

