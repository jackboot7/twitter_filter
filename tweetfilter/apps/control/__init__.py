from apps.channels.models import Channel
from apps.control.tasks import init_channels
print "initializing processes..."

#init_channels.delay()
"""
channels = Channel.objects.filter(status=Channel.STATUS_ENABLED)
for channel in channels:
    channel.is_streaming()
    if not channel.is_streaming():
        channel.init_streaming()
"""