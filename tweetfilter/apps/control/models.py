from django.db import models
#from apps.channels.models import Channel
#from picklefield.fields import PickledObjectField

"""
class Process(models.Model):
    TYPE_STREAMING = 1
    TYPE_DM_FETCH = 2

    TYPE_CHOICES = (
        (TYPE_STREAMING, "Streaming"),
        (TYPE_DM_FETCH, "DM Fetch")
    )

    task_result = PickledObjectField()
    channel = models.ForeignKey(Channel)
    running_since = models.DateTimeField(auto_now=True)
    type = models.IntegerField(choices=TYPE_CHOICES)
"""

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