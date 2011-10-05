import datetime
import re
import time

from django.shortcuts import get_object_or_404
from django.views import generic

from .models import Channel, Event, Link

DATE_RE = re.compile(r'^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})$')

class PublicChannelsMixin(object):
    def get_queryset(self):
        qs = super(PublicChannelsMixin, self).get_queryset()
        if self.request.user.is_authenticated():
            return qs
        return qs.filter(public=True)


class Channels(PublicChannelsMixin, generic.ListView):
    context_object_name = 'channels'
    model = Channel
channels_list = Channels.as_view()


class ChannelView(PublicChannelsMixin, generic.DetailView):
    model = Channel

    def get_object(self):
        qs = super(ChannelView, self).get_queryset()
        return get_object_or_404(qs, name='#' + self.kwargs['channel'])

    def get_context_data(self, **kwargs):
        ctx = super(ChannelView, self).get_context_data(**kwargs)
        filter_date = datetime.datetime.now()
        if 'date' in self.request.GET:
            match = DATE_RE.match(self.request.GET['date'])
            if match:
                timetuple = map(int, match.group(1, 2, 3)) + [0, 0, 0, 0, 0, 0]
                timestamp = time.mktime(timetuple)
                filter_date = datetime.datetime.fromtimestamp(timestamp)
        events = self.object.events.filter(timestamp__year=filter_date.year,
                                           timestamp__month=filter_date.month,
                                           timestamp__day=filter_date.day)
        ctx.update({
            'channels': self.get_queryset(),
            'events': events.reverse(),
            'date': filter_date,
        })
        before = filter_date - datetime.timedelta(days=1)
        after = filter_date + datetime.timedelta(days=1)
        if self.object.events.filter(timestamp__lt=before).exists():
            ctx['before'] = before
        if self.object.events.filter(timestamp__gt=after):
            ctx['after'] = after
        return ctx


class ChannelDetail(ChannelView):
    pass
channel_detail = ChannelDetail.as_view()


class ChannelLinks(generic.ListView):
    model = Link
channel_links = ChannelLinks.as_view()


class Stats(ChannelView):
    pass
channel_stats = Stats.as_view()

