from django.contrib.auth.models import User
from django.db import models

# Create your models here.

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

#
# Singleton config table-row
#
class Config(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(Config, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

    app_key = models.CharField(max_length=64)
    app_secret = models.CharField(max_length=64)
    access_token = models.CharField(max_length=128)     # for OAUTH 2.0
