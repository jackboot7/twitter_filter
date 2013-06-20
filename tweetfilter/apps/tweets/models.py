from django.db import models


class Tweet(models.Model):
    text = models.TextField(max_length=140)
    screen_name = models.TextField(max_length=16)
    tweet_id = models.TextField(max_length=32)
    source = models.TextField(max_length=128)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    hashtags = models.TextField(max_length=140, blank=True)
    media_urls = models.TextField(max_length=140, blank=True)
