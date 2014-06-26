from django.db import models

from apps.accounts.models import Channel
from apps.control.models import ScheduleBlock


class HashtagAdvertisement(ScheduleBlock):
	"""
	A hashtag intended to serve as advertising. It embeds into tweets as long as there is enough space in it and current time
	occurs within the scope of the scheduled block defined
	"""
    channel = models.ForeignKey(Channel, blank=True, null=True)
    text = models.CharField(max_length=32)
    quantity = models.IntegerField()
    count = models.IntegerField(default=0)
    enabled = models.BooleanField(default=True)