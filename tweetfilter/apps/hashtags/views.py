import json
import logging
import datetime

from braces.views import JSONResponseMixin, AjaxResponseMixin, CsrfExemptMixin, LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.list import ListView

from apps.accounts.models import Channel, ItemGroup
from apps.hashtags.models import HashtagAdvertisement


logger = logging.getLogger('app')


class HashtagsHomeView(LoginRequiredMixin, ListView):
    """
    Renders the main interface for hashtags module config
    """
    template_name = "hashtags/settings.html"
    queryset = ItemGroup.objects.filter(channel_exclusive=False)

    def get_context_data(self, **kwargs):
        context = super(HashtagsHomeView, self).get_context_data(**kwargs)
        context['hashtag_groups'] = self.get_queryset().filter(content_type="Hashtag")
        context['channel_list'] = Channel.objects.filter(user_id=self.request.user.id)
        return context


class HashtagsDetailView(LoginRequiredMixin, DetailView):
    model = Channel
    template_name = "hashtags/channel_index.html"
    context_object_name = "channel"

    def get_context_data(self, **kwargs):
        groups_queryset = ItemGroup.objects.filter(channel_exclusive=False)
        context = super(HashtagsDetailView, self).get_context_data(**kwargs)
        context['hashtag_groups'] = groups_queryset.filter(content_type="Hashtag")
        return context


class CheckStatusView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    """
    Returns scheduling module status (is it enabled or disabled?)
    """
    model = Channel

    def get_ajax(self, request,  *args, **kwargs):
        obj = self.get_object()

        if obj.hashtags_enabled:
            response_data = {'result': "enabled"}
        else:
            response_data = {'result': "disabled"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchStatusView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Enables or disables automatic retweets
    """
    model = Channel

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()

        try:
            if obj.hashtags_enabled:
                # disable
                obj.hashtags_enabled = False
                obj.save()
            else:
                # enable
                obj.hashtags_enabled = True
                obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in hashtags.views.SwitchStatusView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class HashtagListView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DetailView):
    model = ItemGroup
    context_object_name = "hashtag_list"

    def get_ajax(self, request, *args, **kwargs):
        objs = HashtagAdvertisement.objects.filter(group=self.get_object())
        json_list = []

        for hashtag in objs:
            dict = model_to_dict(hashtag)
            dict['start'] = hashtag.start.strftime("%H:%M")
            dict['end'] = hashtag.end.strftime("%H:%M")
            json_list.append(dict)

        return self.render_json_response(json_list)


class HashtagCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = HashtagAdvertisement

    def post_ajax(self, request, *args, **kwargs):

        try:        
            group = ItemGroup.objects.filter(id=request.POST['group_id'])[0]

            hashtag = HashtagAdvertisement()
            hashtag.group = group
            hashtag.text = request.POST['text']
            hashtag.quantity = request.POST['qty']
            hashtag.start = datetime.datetime.strptime(request.POST['start'], "%H:%M").time()
            hashtag.end = datetime.datetime.strptime(request.POST['end'], "%H:%M").time()
            hashtag.monday = True if request.POST['monday'] == "1" else False
            hashtag.tuesday = True if request.POST['tuesday'] == "1" else False
            hashtag.wednesday = True if request.POST['wednesday'] == "1" else False
            hashtag.thursday = True if request.POST['thursday'] == "1" else False
            hashtag.friday = True if request.POST['friday'] == "1" else False
            hashtag.saturday = True if request.POST['saturday'] == "1" else False
            hashtag.sunday = True if request.POST['sunday'] == "1" else False
            hashtag.save()
            response_data = {'result': "ok"}
        except Exception, e:
            logger.exception("Error while creating hashtag: %s" % e.args[0])
            response_data = {'result': e.args[0]}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")

class HashtagDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = HashtagAdvertisement
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class HashtagUpdateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    model = HashtagAdvertisement

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.text = request.POST['text']
            obj.quantity = request.POST['qty']
            obj.start = datetime.datetime.strptime(request.POST['start'], "%H:%M").time()
            obj.end = datetime.datetime.strptime(request.POST['end'], "%H:%M").time()
            obj.monday = True if request.POST['monday'] == "1" else False
            obj.tuesday = True if request.POST['tuesday'] == "1" else False
            obj.wednesday = True if request.POST['wednesday'] == "1" else False
            obj.thursday = True if request.POST['thursday'] == "1" else False
            obj.friday = True if request.POST['friday'] == "1" else False
            obj.saturday = True if request.POST['saturday'] == "1" else False
            obj.sunday = True if request.POST['sunday'] == "1" else False
            obj.save()
            response_data = {'result': "ok"}
        except Exception, e:
            response_data = {'result': e.args[0]}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class HashtagResetView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    model = HashtagAdvertisement

    def post_ajax(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            obj.count = 0
            obj.save()
            response_data = {'result': "ok"}
        except Exception, e:
            response_data = {'result': "fail", 'exception': e.args[0]}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


#==============
# Groups views
#==============

class HashtagGroupCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    """
    Creates a new Hashtag group
    """
    model = ItemGroup

    def post_ajax(self, request, *args, **kwargs):
        try:
            hashtag_groups = ItemGroup.objects.filter(content_type="Hashtag")
            for group in hashtag_groups:
                if group.name == request.POST['hashtag_group_name']:
                    response_data = {'result': "duplicate"}
                    break
            else:
                new_group = ItemGroup()
                new_group.content_type = "Hashtag"
                new_group.name = request.POST['hashtag_group_name']
                new_group.save()
                response_data = {'result': "ok", 'group_obj': model_to_dict(new_group)}
        except Exception, e:
            logger.exception("Error al crear grupo de Hashtag")
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class HashtagGroupUpdateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Update Hashtag group attributes
    """
    model = ItemGroup

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            hashtag_groups = ItemGroup.objects.filter(content_type="Hashtag").exclude(id=obj.id)
            for group in hashtag_groups:
                if group.name == request.POST['hashtag_group_name']:
                    response_data = {'result': "duplicate"}
                    break
            else:
                obj.name = request.POST['hashtag_group_name']
                obj.save()
                response_data = {'result': "ok"}
        except Exception, e:
            response_data = {'result': e.args[0]}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class HashtagGroupListView(JSONResponseMixin, AjaxResponseMixin, ListView):
    """
    Shows a all non-exclusive Hashtag groups
    """
    queryset = ItemGroup.objects.filter(content_type="Hashtag").filter(channel_exclusive=False)

    def get_ajax(self, request, *args, **kwargs):
        json_list = []
        group_list = self.get_queryset()

        for group in group_list:
            group_dict = model_to_dict(group)
            group_dict['channels'] = []
            
            for chan in group.channel_set.all():
                group_dict['channels'].append(chan.screen_name)
            
            json_list.append(group_dict)

        return self.render_json_response(json_list)


class SetItemGroupChannelsView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Associates a list of channels to the item group
    """
    model = ItemGroup

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            channels = json.loads(request.POST['channels'])
            obj.channel_set.clear()
            
            for chan in channels:
                obj.channel_set.add(chan)

            obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in SwitchStatusView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ItemGroupChannelListView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    """
    Given an item group, returns all channels associated with it
    """
    model = ItemGroup

    def get_ajax(self, request,  *args, **kwargs):
        obj = self.get_object()
        response_data = []
        
        for chan in obj.channel_set.all():
            response_data.append(chan.screen_name)

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ItemGroupDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    """
    Deletes an item group
    """
    model = ItemGroup
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ChannelUnlinkGroupView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Removes the association between a channel and an ItemGroup
    """
    model = Channel

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            obj.groups.remove(request.POST['group_id'])
            
            obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in ChannelUnlinkGroupView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SetChannelGroupsView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Associates a list of groups to the channel
    """
    model = Channel

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            linked_groups = obj.groups.filter(content_type=request.POST['content_type']).exclude(channel_exclusive=True)
            new_groups = json.loads(request.POST['groups'])

            obj.groups.remove(*linked_groups)
            
            if new_groups:
                obj.groups.add(*new_groups)
            
            obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in SetChannelGroupsView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ListChannelGroupsView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    """
    Given an item group, returns all channels associated with it
    """
    model = Channel

    def get_ajax(self, request,  *args, **kwargs):
        obj = self.get_object()
        response_data = []
        
        for group in obj.groups.filter(content_type=request.GET['content_type']):
            response_data.append(group.id)

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class HashtagGroupListChannelView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    """
    Shows a all hashtag groups linked to a particular channel
    """
    model = Channel

    def get_ajax(self, request, *args, **kwargs):
        json_list = []
        group_list = self.get_object().groups.filter(content_type="Hashtag")

        for group in group_list:
            group_dict = model_to_dict(group)
            json_list.append(group_dict)

        return self.render_json_response(json_list)
