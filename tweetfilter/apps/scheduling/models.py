from django.db import models
from apps.accounts.models import Channel
from apps.control.models import ScheduleBlock

class ScheduledTweet(models.Model):
    STATUS_DISABLED = 0
    STATUS_ENABLED = 1

    STATUS_CHOICES = (
        (STATUS_DISABLED, "Desactivado"),
        (STATUS_ENABLED, "Activado")
    )

    text = models.CharField(max_length=140)
    schedule = models.ForeignKey(ScheduleBlock)
    channel = models.ForeignKey(Channel)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ENABLED)