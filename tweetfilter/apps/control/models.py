from celery.backends.database.models import Task
from celery.schedules import crontab
from django.db import models
from django.utils.timezone import now
from djcelery.models import PeriodicTask


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


class OneTimeTask(Task):
    start_time = models.DateTimeField()

    def __init__(self, time):
        super(OneTimeTask, self).__init__()
        self.track_started = True   # useful for streaming tasks (initializes as started instead of pending)
        self.start = time

    def __call__(self, *args, **kwargs):
        # calculate eta to start_stime, self.delay(eta)
        return self.run(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        #exit point
        pass


class RepeatTask(PeriodicTask):
    start_time = models.TimeField()
    start_crontab = {}

    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    def __init__(self, time):
        super(RepeatTask, self).__init__()
        self.start = time

    def __call__(self, *args, **kwargs):

        self.start_crontab = crontab(
            hour=self.start_time.hour,
            minute=self.start_time.minute,
            day_of_week=self.days_of_week_list())
        # add schedule with crontab

        return self.run(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

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


class IntervalTask(RepeatTask):
    end_time = models.TimeField()
    start_crontab = {}
    end_crontab = {}
    # associate with TimeBlock ???

    def __init__(self, time):
        super(IntervalTask, self).__init__()
        self.start = time

    def __call__(self, *args, **kwargs):
        # calculate start_crontab and end_crontab
        if self.start_time <= now() <= self.end_time and now().day in self.days_of_week_list():
            return self.run(*args, **kwargs)
        else:
            # delay until next start_time
            pass


    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

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