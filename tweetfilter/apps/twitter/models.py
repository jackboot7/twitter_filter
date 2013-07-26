from django.db import models
import time


class Tweet(models.Model):
    STATUS_PENDING = 0
    STATUS_APPROVED = 1
    STATUS_BLOCKED = 2
    STATUS_SENT = 3
    STATUS_TRIGGERED = 4
    STATUS_NOT_TRIGGERED = 5

    TYPE_MENTION = 0
    TYPE_DM = 1

    TYPE_CHOICES = (
        (TYPE_MENTION, "Mention"),
        (TYPE_DM, "DM")
    )

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_APPROVED, 'Aprobado'),
        (STATUS_BLOCKED, 'Bloqueado'),
        (STATUS_SENT, 'Enviado')
    )

    text = models.CharField(max_length=140)
    screen_name = models.CharField(max_length=16)
    tweet_id = models.CharField(max_length=32, unique=True)
    source = models.CharField(max_length=128)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    hashtags = models.CharField(max_length=140, blank=True)
    media_urls = models.CharField(max_length=140, blank=True)
    mention_to = models.CharField(max_length=16)
    status = models.SmallIntegerField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
    type = models.SmallIntegerField(max_length=2, choices=TYPE_CHOICES)
    retweeted_text = models.CharField(max_length=140, blank=True)

    def get_excerpt(self):
        max_chars = 32
        date_time = self.date_time.strftime('%d/%m/%y %H:%M:%S')
        return "%s %s..." % (date_time, self.retweeted_text[0:max_chars])