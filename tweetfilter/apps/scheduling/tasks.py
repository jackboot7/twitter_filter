from celery.task.base import task
from django.conf import settings
from apps.accounts.models import Channel
from apps.twitter.api import Twitter

@task(queue="scheduling")
def schedule_tweet(channel_id, text):
    print "sending scheduled tweet for %s" % channel_id
    channel = Channel.objects.filter(screen_name=channel_id)[0]
    twitter = Twitter(
        key=settings.TWITTER_APP_KEY,
        secret=settings.TWITTER_APP_SECRET,
        token=channel.oauth_token,
        token_secret=channel.oauth_secret)
    twitter.tweet(text)
    # capturar errores?