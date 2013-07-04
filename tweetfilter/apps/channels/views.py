# Create your views here.
from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import ListView
from apps.channels.models import Channel

class ChannelListView(JSONResponseMixin, AjaxResponseMixin, ListView):
    model = Channel
    context_object_name = "channel_list"

    def get_ajax(self, request, *args, **kwargs):
        objs = Channel.objects.all()
        json_list = []

        for channel in objs:
            last_tweet = channel.get_last_update()
            json_list.append({
                'screen_name': channel.screen_name,
                'last_tweet': last_tweet.get_excerpt(),
                'status' : last_tweet.get_status_display()
            })

        return self.render_json_response(json_list)

"""
def xhr_test(request, format):
    objs = Channel.objects.all()
    if request.is_ajax():
        data = serializers.serialize('json', objs)
        return HttpResponse(data,'json')
    else:
        return render_to_response('template.html', {'channel_list':objs}, context=...)
"""