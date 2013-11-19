from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from apps.accounts.models import Channel

class Notification(models.Model):
    recipient = models.ForeignKey(User)
    channel = models.ForeignKey(Channel, blank=True, null=True)
    description = models.TextField(max_length=140)
    url = models.URLField(blank=True, null=True)

    read = models.BooleanField(default=False)

