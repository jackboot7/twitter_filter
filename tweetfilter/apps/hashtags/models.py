from django.db import models

from apps.accounts.models import Channel, ItemGroup
from apps.control.models import ScheduleBlock


class HashtagAdvertisement(ScheduleBlock):
    """
    A suffix intended to serve as advertising or specific notifications. It embeds into tweets as long as 
    there is enough space in it and current time is within the scope of the scheduled block defined
    """
    STATUS_DISABLED = 0
    STATUS_ENABLED = 1

    STATUS_CHOICES = (
        (STATUS_DISABLED, "Desactivado"),
        (STATUS_ENABLED, "Activado")
    )

    group = models.ForeignKey(ItemGroup, blank=True, null=True)
    text = models.CharField(max_length=32)
    quantity = models.IntegerField()
    count = models.IntegerField(default=0)
    enabled = models.BooleanField(default=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ENABLED)
