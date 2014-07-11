from celery.task.base import task
from django.conf import settings
from apps.accounts.models import ItemGroup 
from apps.twitter.api import Twitter

@task(queue="tweets", ignore_result=True)
def schedule_tweet(group_id, text):
    group = ItemGroup.objects.get(group_id)
    for channel in group.channel_set.all():
        if channel.scheduling_enabled:
            twitter = Twitter(
                key=settings.TWITTER_APP_KEY,
                secret=settings.TWITTER_APP_SECRET,
                token=channel.oauth_token,
                token_secret=channel.oauth_secret)
            twitter.tweet(text)

