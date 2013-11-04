from django.views.generic.detail import DetailView
from apps.accounts.models import Channel

class HashtagsDetailView(DetailView):
    model = Channel
    template_name = "hashtags/index.html"
    context_object_name = "channel"