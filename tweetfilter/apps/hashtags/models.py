from django.db import models

# Create your models here.
from apps.accounts.models import Channel

from apps.control.models import ScheduleBlock

class HashtagAdvertisement(models.Model):
    channel = models.ForeignKey(Channel, blank=True, null=True)
    text = models.CharField(max_length=32)
    schedule = models.ForeignKey(ScheduleBlock)
    quantity = models.IntegerField()
    enabled = models.BooleanField(default=True)