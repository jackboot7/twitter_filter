from django.db import models


class Tweet(models.Model):
    PENDING_STATUS = 0
    APPROVED_STATUS = 1
    BLOCKED_STATUS = 2
    SENT_STATUS = 3

    STATUS_CHOICES = (
        (PENDING_STATUS, 'Pendiente'),
        (APPROVED_STATUS, 'Aprobado'),
        (BLOCKED_STATUS, 'Bloqueado'),
        (SENT_STATUS, 'Enviado')
    )

    text = models.CharField(max_length=140)
    screen_name = models.CharField(max_length=16)
    tweet_id = models.CharField(max_length=32, unique=True)
    source = models.CharField(max_length=128)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    hashtags = models.CharField(max_length=140, blank=True)
    media_urls = models.CharField(max_length=140, blank=True)
    status = models.SmallIntegerField(max_length=16, choices=STATUS_CHOICES, default=PENDING_STATUS)
