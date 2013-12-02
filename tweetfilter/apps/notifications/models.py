import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models

# Create your models here.
from apps.accounts.models import Channel


class Notification(models.Model):
    recipient = models.ForeignKey(User)
    channel = models.ForeignKey(Channel, blank=True, null=True)
    description = models.TextField(max_length=140)
    url = models.URLField(blank=True, null=True)

    time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    read = models.BooleanField(default=False)

    @classmethod
    def create(cls, user, channel=None, desc=""):
        notify = cls(recipient=user)
        notify.channel = channel
        notify.description = desc
        notify.time = datetime.datetime.now()
        return notify

    def mail_user(self, subject, extra):
        from apps.notifications import tasks
        tasks.send_mail_notification.delay(self.recipient.email, self, subject, extra)

