from django.contrib.auth.models import User
from django.db import models

# Create your models here.
import django.db.models
from apps.twitter.models import Tweet

class Channel(models.Model):
    DISABLED_STATUS = 0
    ENABLED_STATUS = 1

    STATUS_CHOICES = (
        (DISABLED_STATUS, 'Inactivo'),
        (ENABLED_STATUS, 'Activo')
    )

    screen_name = models.CharField(max_length=16)
    oauth_token = models.CharField(max_length=128)
    oauth_secret = models.CharField(max_length=128)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=ENABLED_STATUS)
    user = models.ForeignKey(User, blank=True, null=True)

    def get_last_update(self):
        update = Tweet.objects.filter(status=Tweet.SENT_STATUS, mention_to=self.screen_name).order_by('-id')[0]

    def activate(self):
        self.status = self.ENABLED_STATUS
        self.save()

    def deactivate(self):
        self.status = self.DISABLED_STATUS
        self.save()
