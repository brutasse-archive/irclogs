import datetime
import os
import re
import time

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Channel, Event

CHAN_RE = re.compile(r'^(.+)_(\d{4})(\d{2})(\d{2}).log$')
LINE_RE = re.compile(r'^\[(\d{2}):(\d{2}):(\d{2})\] (.+)$')
JOIN_QUIT_RE = re.compile(r'^\*\*\* (Joins|Quits|Parts): ([^\s]+) (.+)$')
NICK_RE = re.compile(r'^\*\*\* ([^\s]+) is now known as ([^\s]+)$')
MODE_RE = re.compile(r'^\*\*\* ([^\s]+) (.+)$')
MSG_RE = re.compile(r'^<([^\s]+)> (.+)$')
ME_RE = re.compile(r'^\* ([^\s]+) (.+)$')

EVENT_TYPES = {
    'Joins': Event.JOIN,
    'Quits': Event.QUIT,
    'Parts': Event.PART,
}


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-a', '--all', action='store_true', dest='all',
                    default=False),
    )

    def handle(self, *args, **options):
        for f in sorted(os.listdir(settings.LOGS_DIR)):
            self.handle_file(f, options['all'])

        print Channel.objects.count(), "channels"
        print Event.objects.count(), "events"

    def handle_file(self, file_, all_):
        full_path = os.path.join(settings.LOGS_DIR, file_)
        name, year, month, day = CHAN_RE.match(file_).group(1, 2, 3, 4)
        date = (year, month, day)
        if datetime.date(*map(int, date)) + datetime.timedelta(days=1) < datetime.date.today() and not all_:
            return
        print file_
        channel, created = Channel.objects.get_or_create(name=name)
        with open(full_path, 'r') as f:
            self.parse_file(f, file_, date, channel)

    def parse_file(self, fd, file_, date, channel):
        length = len(fd.readlines())  # zero-based
        if Event.objects.filter(filename=file_, lineno=length-1).exists():
            # This file has alaready been fully processed
            return

        fd.seek(0)
        for index, line in enumerate(fd):
            hour, minute, second, msg = LINE_RE.match(line).group(1, 2, 3, 4)
            timetuple = map(int, date + (hour, minute, second, 0, 0, 0))
            timestamp = time.mktime(timetuple) + 3600
            real_date = datetime.datetime.fromtimestamp(timestamp)

            join_quit = JOIN_QUIT_RE.match(msg)
            mode = MODE_RE.match(msg)
            message = MSG_RE.match(msg)
            nick = NICK_RE.match(msg)
            me = ME_RE.match(msg)

            if join_quit:
                action, user, message = join_quit.group(1, 2 ,3)
                event_type=EVENT_TYPES[action]
            elif nick:
                user, message = nick.group(1, 2)
                message = 'is now known as ' + message
                event_type = Event.NICK
            elif mode:
                user, message = mode.group(1, 2)
                event_type = Event.MODE
            elif message:
                user, message = message.group(1, 2)
                event_type = Event.CHAT
            elif me:
                user, message = me.group(1, 2)
                event_type = Event.ME
            else:
                print "IGNORED:", msg
                continue

            try:
                message = message.decode('utf-8')
            except UnicodeDecodeError:
                message = message.decode('iso8859-15')

            Event.objects.get_or_create(
                channel=channel,
                event_type=event_type,
                nickname=user,
                content=message,
                timestamp=real_date,
                filename=file_,
                lineno=index,
            )
