from django.db import models

# Create your models here.

from apps.control.models import ScheduleBlock

class HashtagAdvertisement(models.Model):
    text = models.CharField(max_length=32)
    schedule = models.ForeignKey(ScheduleBlock)
    quantity = models.IntegerField()
    enabled = models.BooleanField(default=True)