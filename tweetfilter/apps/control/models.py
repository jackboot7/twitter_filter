#from django.db import models
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