# from django.db import models

# Create your models here.



"""
class BlockedUser(models.Model):
    screen_name = models.CharField(max_length=16)
    block_date = models.DateTimeField(auto_now=True)
    block_duration = models.IntegerField()
    reason = models.CharField(max_length=64)
    channel = models.ForeignKey(Channel)

# Lista "blanca"
class AllowedUser(models.Model):
    screen_name = models.CharField(max_length=16)
    channel = models.ForeignKey(Channel)
"""