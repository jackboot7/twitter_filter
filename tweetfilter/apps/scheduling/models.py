from django.db import models
from apps.accounts.models import Channel
from apps.control.models import ScheduleBlock, Schedule

class ScheduledTweet(Schedule):
    STATUS_DISABLED = 0
    STATUS_ENABLED = 1

    STATUS_CHOICES = (
        (STATUS_DISABLED, "Desactivado"),
        (STATUS_ENABLED, "Activado")
    )

    text = models.CharField(max_length=140)
    channel = models.ForeignKey(Channel)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ENABLED)

    def get_excerpt(self):
        max_chars = 32
        return self.text[0:max_chars]