from celery.task.base import task
from django.conf import settings
from apps.scheduling.models import ScheduledTweet 
from apps.twitter.api import Twitter

@task(queue="tweets", ignore_result=True)
def schedule_tweet(scheduled_tweet_id):
    tweet = ScheduledTweet.objects.get(id=scheduled_tweet_id)

    if tweet.status == ScheduledTweet.STATUS_ENABLED:
        group = tweet.group
        for channel in group.channel_set.all():
            if channel.scheduling_enabled:
                twitter = Twitter(
                    key=settings.TWITTER_APP_KEY,
                    secret=settings.TWITTER_APP_SECRET,
                    token=channel.oauth_token,
                    token_secret=channel.oauth_secret)
                twitter.tweet(tweet.text)

