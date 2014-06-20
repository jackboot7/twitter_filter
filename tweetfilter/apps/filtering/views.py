import datetime
from exceptions import Exception
import json
import logging
from braces.views import AjaxResponseMixin, JSONResponseMixin, CsrfExemptMixin, LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.views.generic import DetailView, View, DeleteView
from django.views.generic.edit import UpdateView
from apps.accounts.models import Channel
from apps.control.models import ScheduleBlock
from apps.filtering import tasks
from apps.filtering.models import BlockedUser, Trigger, Filter, ChannelScheduleBlock, Replacement, Keyword

logger = logging.getLogger('app')

class FilteringDetailView(LoginRequiredMixin, DetailView):
    """
    Renders the main interface for filtering module config
    """
    model = Channel
    template_name = "filtering/index.html"
    context_object_name = "channel"


#==========================
# Filtering Config
#==========================
class CheckStatusView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    """
    Returns filtering module status (is it enabled or disabled?)
    """
    model = Channel

    def get_ajax(self, request,  *args, **kwargs):
        obj = self.get_object()
        response_data = {'module_enabled': obj.retweets_enabled,
                         'scheduled_blocks': obj.scheduleblocks_enabled,
                         'blacklist':  obj.blacklist_enabled,
                         'triggers': obj.triggers_enabled,
                         'replacements': obj.replacements_enabled,
                         'filters': obj.filters_enabled
        }

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
            if obj.retweets_enabled:
                # if enabled: disable.
                if obj.stop_streaming():
                    obj.retweets_enabled = False
                    obj.save()
                    response_data = {'result': "ok"}
                else:
                    response_data = {'result': "fail"}
            else:
                # else: enable
                if obj.init_streaming():
                    obj.retweets_enabled = True
                    obj.save()
                    response_data = {'result': "ok"}
                else:
                    response_data = {'result': "fail"}

        except Exception as e:
            logger.exception("Error in SwitchStatusView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchScheduleBlocksView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Enables or disables filtering by time schedule blocks
    """
    model = Channel

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()

        try:
            if obj.scheduleblocks_enabled:
                # disable
                obj.scheduleblocks_enabled = False
                obj.save()
            else:
                # enable
                obj.scheduleblocks_enabled = True
                obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in SwitchScheduleBlocksView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchBlackListView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Enables or disables blocking blacklisted users
    """
    model = Channel

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()

        try:
            if obj.blacklist_enabled:
                # disable
                obj.blacklist_enabled = False
                obj.save()
            else:
                # enable
                obj.blacklist_enabled = True
                obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in SwitchBlackListView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")



class SwitchTriggersView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Enables or disables filtering by triggers
    """
    model = Channel

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()

        try:
            if obj.triggers_enabled:
                # disable
                obj.triggers_enabled = False
                obj.save()
            else:
                # enable
                obj.triggers_enabled = True
                obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in SwitchTriggersView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchReplacementsView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Enables or disables word replacing
    """
    model = Channel

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()

        try:
            if obj.replacements_enabled:
                # disable
                obj.replacements_enabled = False
                obj.save()
            else:
                # enable
                obj.replacements_enabled = True
                obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in SwitchReplacementsView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchFiltersView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Enables or disables banned words filter
    """
    model = Channel

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()

        try:
            if obj.filters_enabled:
                # disable
                obj.filters_enabled = False
                obj.save()
            else:
                # enable
                obj.filters_enabled = True
                obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in SwitchFiltersView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchTriggerMentionView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    model = Trigger
    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            if obj.enabled_mentions:
                obj.enabled_mentions = False
            else:
                obj.enabled_mentions = True
            obj.save()
            response_data = {'result': "ok"}
        except Exception:
            logger.exception("Error in SwitchKeywordMentionView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchTriggerDMView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    model = Trigger
    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            if obj.enabled_dm:
                obj.enabled_dm = False
            else:
                obj.enabled_dm = True
            obj.save()
            response_data = {'result': "ok"}
        except Exception:
            logger.exception("Error in SwitchKeywordDMView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchFilterMentionView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    model = Filter
    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            if obj.enabled_mentions:
                obj.enabled_mentions = False
            else:
                obj.enabled_mentions = True
            obj.save()
            response_data = {'result': "ok"}
        except Exception:
            logger.exception("Error in SwitchFilterMentionView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchFilterDMView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    model = Filter
    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            if obj.enabled_dm:
                obj.enabled_dm = False
                obj.save()
            else:
                obj.enabled_dm = True
            obj.save()
            response_data = {'result': "ok"}
        except Exception:
            logger.exception("Error in SwitchFilterDMView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchReplacementMentionView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    model = Replacement
    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            if obj.enabled_mentions:
                obj.enabled_mentions = False
            else:
                obj.enabled_mentions = True
            obj.save()
            response_data = {'result': "ok"}
        except Exception:
            logger.exception("Error in SwitchReplacementMentionView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchReplacementDMView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    model = Replacement
    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            if obj.enabled_dm:
                obj.enabled_dm = False
            else:
                obj.enabled_dm = True
            obj.save()
            response_data = {'result': "ok"}
        except Exception:
            logger.exception("Error in SwitchReplacementDMView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class SwitchUpdateLimitView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    """
    Enables or disables update limit prevention
    """
    model = Channel

    def post_ajax(self, request, *args, **kwargs):
        obj = self.get_object()

        try:
            if obj.prevent_update_limit:
                # disable
                obj.prevent_update_limit = False
                obj.save()
            else:
                # enable
                obj.prevent_update_limit = True
                obj.save()
            response_data = {'result': "ok"}
        except Exception as e:
            logger.exception("Error in SwitchUpdateLimitView")
            response_data = {'result': "fail"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")

#==========================
# Trigger words
#==========================

class TriggerCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = Trigger

    def post_ajax(self, request, *args, **kwargs):

        try:
            triggers = Trigger.objects.filter(channel=request.POST['trigger_channel'])
            for tr in triggers:
                if tr.equals(request.POST['trigger_text']):
                    response_data = {'result': "duplicate"}
                    break
            else:
                chan = Channel.objects.filter(screen_name=request.POST['trigger_channel'])[0]
                trigger = Trigger()
                trigger.text = request.POST['trigger_text']
                trigger.channel = chan
                trigger.save()
                response_data = {'result': "ok"}
        except Exception, e:
            logger.exception("Error al crear trigger")
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class TriggerListView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    model = Channel

    def get_ajax(self, request, *args, **kwargs):
        objs = Trigger.objects.filter(channel=self.get_object()).order_by("text")

        json_list = []
        for trigger in objs:
            dict = model_to_dict(trigger)
            json_list.append(dict)

        return self.render_json_response(json_list)
        #return self.render_json_response(objs)


class TriggerDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = Trigger
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


#==========================
# Replacement words
#==========================

class ReplacementCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = Replacement

    def post_ajax(self, request, *args, **kwargs):

        try:
            reps = Replacement.objects.filter(channel=request.POST['replacement_channel'])
            for rp in reps:
                if rp.equals(request.POST['replacement_text']):
                    response_data = {'result': "duplicate"}
                    break
            else:
                chan = Channel.objects.filter(screen_name=request.POST['replacement_channel'])[0]
                replacement = Replacement()
                replacement.text = request.POST['replacement_text']
                replacement.replace_with = request.POST['replacement_replace_with']
                replacement.channel = chan
                replacement.save()
                response_data = {'result': "ok"}
        except Exception, e:
            logger.exception("Error al crear supresor")
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class ReplacementListView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    model = Channel

    def get_ajax(self, request, *args, **kwargs):
        objs = Replacement.objects.filter(channel=self.get_object()).order_by("text")
        json_list = []

        for rep in objs:
            dict = model_to_dict(rep)
            json_list.append(dict)

        return self.render_json_response(json_list)


class ReplacementDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = Replacement
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


#==========================
# Forbidden word filters
#==========================

class FilterCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = Filter

    def post_ajax(self, request, *args, **kwargs):

        try:
            filters = Filter.objects.filter(channel=request.POST['filter_channel'])
            for fl in filters:
                if fl.equals(request.POST['filter_text']):
                    response_data = {'result': "duplicate"}
                    break
            else:
                chan = Channel.objects.filter(screen_name=request.POST['filter_channel'])[0]
                filter = Filter()
                filter.text = request.POST['filter_text']
                filter.channel = chan
                filter.save()
                response_data = {'result': "ok"}
        except Exception, e:
            logger.exception("Error al crear filter")
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class FilterListView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    model = Channel

    def get_ajax(self, request, *args, **kwargs):
        objs = Filter.objects.filter(channel=self.get_object()).order_by("text")

        json_list = []
        for trigger in objs:
            dict = model_to_dict(trigger)
            json_list.append(dict)

        return self.render_json_response(json_list)
        #return self.render_json_response(objs)


class FilterDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = Filter
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


#==========================
# Blocked users (blacklist)
#==========================

class BlockedUserListView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    model = Channel

    def get_ajax(self, request, *args, **kwargs):
        objs = BlockedUser.objects.filter(channel=self.get_object()).order_by("screen_name")

        json_list = []
        for user in objs:
            dict = model_to_dict(user)
            json_list.append(dict)

        return self.render_json_response(json_list)
        #return self.render_json_response(objs)


class BlockedUserDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = BlockedUser
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")

class BlockedUserCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = BlockedUser

    def post_ajax(self, request, *args, **kwargs):
        blocked_users = BlockedUser.objects.filter(channel=request.POST['blocked_user_channel'])
        for bo in blocked_users:
            if bo.screen_name.lower() == request.POST['blocked_user_name'].lower():
                response_data = {'result': "duplicate"}
                break
        else:
            try:
                chan = Channel.objects.filter(screen_name=request.POST['blocked_user_channel'])[0]
                user = BlockedUser()
                user.screen_name = request.POST['blocked_user_name']
                user.channel = chan
                user.save()
                response_data = {'result': "ok"}
            except Exception, e:
                logger.exception("Error al bloquear usuario")
                response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


#=========================
# Time block views
#=========================

class TimeBlockListView(JSONResponseMixin, AjaxResponseMixin, DetailView):
    model = Channel
    context_object_name = "timeblock_list"

    def get_ajax(self, request, *args, **kwargs):
        objs = ChannelScheduleBlock.objects.filter(channel=self.get_object())
        json_list = []

        for timeblock in objs:
            dias = ""
            allows = ""

            if timeblock.monday:
                dias = "Lun "
            if timeblock.tuesday:
                dias += "Mar "
            if timeblock.wednesday:
                dias += "Mie "
            if timeblock.thursday:
                dias += "Jue "
            if timeblock.friday:
                dias += "Vie "
            if timeblock.saturday:
                dias += "Sab "
            if timeblock.sunday:
                dias += "Dom "
            if len(dias) == 28:
                dias = "Todos"

            if timeblock.allow_dm:
                allows = "DM"
                if timeblock.allow_mentions:
                    allows += " y Mentions"
            else:
                allows = "Mentions"

            json_list.append({
                'id': timeblock.id,
                'time': "%s - %s" % (timeblock.start.strftime("%H:%M"), timeblock.end.strftime("%H:%M")),
                'start': timeblock.start.strftime("%H:%M"),
                'end': timeblock.end.strftime("%H:%M"),
                'days': dias,
                'allows': allows,
                'monday': timeblock.monday,
                'tuesday': timeblock.tuesday,
                'wednesday': timeblock.wednesday,
                'thursday': timeblock.thursday,
                'friday': timeblock.friday,
                'saturday': timeblock.saturday,
                'sunday': timeblock.sunday,
                'allow_dm': timeblock.allow_dm,
                'allow_mentions': timeblock.allow_mentions
            })

        return self.render_json_response(json_list)


class TimeBlockCreateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, View):
    model = ScheduleBlock

    def post_ajax(self, request, *args, **kwargs):

        try:
            chan = Channel.objects.filter(screen_name=request.POST['timeblock_channel'])[0]
            block = ChannelScheduleBlock()

            block.start = datetime.datetime.strptime(request.POST['start'], "%H:%M").time()
            block.end = datetime.datetime.strptime(request.POST['end'], "%H:%M").time()

            block.allow_mentions = True if request.POST['allow_mentions'] == "1" else False
            block.allow_dm = True if request.POST['allow_dm'] == "1" else False

            block.monday = True if request.POST['monday'] == "1" else False
            block.tuesday = True if request.POST['tuesday'] == "1" else False
            block.wednesday = True if request.POST['wednesday'] == "1" else False
            block.thursday = True if request.POST['thursday'] == "1" else False
            block.friday = True if request.POST['friday'] == "1" else False
            block.saturday = True if request.POST['saturday'] == "1" else False
            block.sunday = True if request.POST['sunday'] == "1" else False
            block.channel = chan
            block.save()
            response_data = {'result': "ok"}
        except Exception, e:
            logger.exception("Error al crear timeblock")
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")


class TimeBlockDeleteView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, DeleteView):
    model = ScheduleBlock   # ChannelScheduleBlock # ????
    success_url = "/"

    def post_ajax(self, request, *args, **kwargs):
        #obj = self.get_object()
        self.delete(request)
        response_data = {'result': "ok"}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")

class TimeBlockUpdateView(CsrfExemptMixin, JSONResponseMixin,
    AjaxResponseMixin, UpdateView):
    model = ChannelScheduleBlock

    def post_ajax(self, request, *args, **kwargs):
        block = self.get_object()
        try:
            block.start = datetime.datetime.strptime(request.POST['start'], "%H:%M").time()
            block.end = datetime.datetime.strptime(request.POST['end'], "%H:%M").time()

            block.allow_mentions = True if request.POST['allow_mentions'] == "1" else False
            block.allow_dm = True if request.POST['allow_dm'] == "1" else False
            block.monday = True if request.POST['monday'] == "1" else False
            block.tuesday = True if request.POST['tuesday'] == "1" else False
            block.wednesday = True if request.POST['wednesday'] == "1" else False
            block.thursday = True if request.POST['thursday'] == "1" else False
            block.friday = True if request.POST['friday'] == "1" else False
            block.saturday = True if request.POST['saturday'] == "1" else False
            block.sunday = True if request.POST['sunday'] == "1" else False

            block.save()
            response_data = {'result': "ok"}
        except Exception, e:
            response_data = {'result': e}

        return HttpResponse(json.dumps(response_data),
            content_type="application/json")
