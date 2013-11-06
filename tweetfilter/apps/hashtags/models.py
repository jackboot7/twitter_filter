from django.db import models

# Create your models here.
from apps.accounts.models import Channel

from apps.control.models import ScheduleBlock

class HashtagAdvertisement(ScheduleBlock):
    channel = models.ForeignKey(Channel, blank=True, null=True)
    #schedule = models.ForeignKey(ScheduleBlock, blank=True, null=True)
    text = models.CharField(max_length=32)
    quantity = models.IntegerField()
    enabled = models.BooleanField(default=True)