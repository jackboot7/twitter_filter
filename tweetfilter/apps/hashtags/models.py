from django.db import models

# Create your models here.
import django.db.models
from apps.control.models import ScheduleBlock

class HashtagAdvertisement(models.Model):
    text = models.CharField(max_length=32)
    schedule = models.ForeignKey(ScheduleBlock)
    quantity = models.IntegerField()