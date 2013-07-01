from django.db import models


class Tweet(models.Model):
    text = models.CharField(max_length=140)
    screen_name = models.CharField(max_length=16)
    tweet_id = models.CharField(max_length=32, unique=True)
    source = models.CharField(max_length=128)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    hashtags = models.CharField(max_length=140, blank=True)
    media_urls = models.CharField(max_length=140, blank=True)
    status = models.CharField(max_length=16, default="PENDING")
