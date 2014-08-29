from datetime import datetime, timedelta, time

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
    quantity = models.IntegerField()            # DEPRECATED
    count = models.IntegerField(default=0)      # DEPRECATED
    limit = models.IntegerField(default=0)
    enabled = models.BooleanField(default=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ENABLED)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def get_appliances(self, channel_name=None):
        """
        Returns a list of succesful hashtag appliances, optionally filtered by channel
        """
        appliances = self.hashtagappliance_set.all()

        if channel_name:
            return appliances.filter(channel__pk=channel_name)
        else:
            return appliances

    def get_today_count(self, channel_name=None):
        """
        Returns the number of times this hashtag has been applied successfully
        """
        appliances = self.get_appliances(channel_name)
        
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())

        count = appliances.filter(date_time__gte=today_start, date_time__lt=today_end).count()

        return count

    def is_under_daily_limit(self):
        """
        Return True if daily limit is over today's appliance count
        """
        return self.get_today_count() < self.limit

    def get_total_count(self):
        """
        Returns total count of appliances
        """
        return self.get_appliances().count()

    def applies_now(self):
        """
        Return True if current time is inside hashtag time limits
        """
        now = datetime.now()
        return self.start_date <= now.date() <= self.end_date and self.has_datetime(now)


class HashtagAppliance(models.Model):
    """
    Represents a successful application of a hashtag (suffix) into a tweet sent from a Channel
    """
    hashtag = models.ForeignKey(HashtagAdvertisement)
    channel = models.ForeignKey(Channel)
    date_time = models.DateTimeField(auto_now=True)
    # tweet ?

