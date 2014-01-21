from celery.task.base import task
from django.conf import settings
from apps.accounts.models import Channel
from apps.twitter.api import Twitter

@task(queue="tweets", ignore_result=True)
def schedule_tweet(channel_id, text):
    channel = Channel.objects.filter(screen_name=channel_id)[0]
    if channel.scheduling_enabled:
        twitter = Twitter(
            key=settings.TWITTER_APP_KEY,
            secret=settings.TWITTER_APP_SECRET,
            token=channel.oauth_token,
            token_secret=channel.oauth_secret)
        twitter.tweet(text)

