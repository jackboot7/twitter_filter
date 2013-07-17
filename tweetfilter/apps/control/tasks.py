from celery.task.base import task
from apps.channels.models import Channel

@task()
def init_channels():
    channels = Channel.objects.filter(status=Channel.STATUS_ENABLED)
    for channel in channels:
        if not channel.is_streaming():
            channel.init_streaming()