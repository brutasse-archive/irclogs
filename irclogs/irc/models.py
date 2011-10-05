from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Channel(models.Model):
    name = models.CharField(_('Name'), max_length=255, db_index=True)
    public = models.BooleanField(_('Is public'), default=False)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('channel_detail', args=[self.name[1:]])

    def is_public(self):
        return self.name.startswith('#')


class Event(models.Model):
    JOIN = 'JOIN'
    QUIT = 'QUIT'
    PART = 'PART'
    NICK = 'NICK'
    MODE = 'MODE'
    ME = 'ME'
    CHAT = 'CHAT'
    TYPES = (
        (JOIN, _('Join')),
        (QUIT, _('Quit')),
        (PART, _('Part')),
        (NICK, _('Nick')),
        (MODE, _('Mode')),
        (ME, _('Me')),
        (CHAT, _('Chat')),
    )

    TYPES_SUBST = {
        JOIN: u'*** Joins:',
        QUIT: u'*** Quits:',
        PART: u'*** Parts:',
    }
    channel = models.ForeignKey(Channel, verbose_name=_('Channel'),
                                related_name='events')
    event_type = models.CharField(_('Event type'), choices=TYPES,
                                  db_index=True, max_length=10)
    nickname = models.CharField(_('Nickname'), max_length=255, db_index=True)
    content = models.TextField(_('Content'))
    timestamp = models.DateTimeField(_('Date'), db_index=True)

    # Where is this in the log?
    filename = models.CharField(_('Filename'), max_length=255, db_index=True)
    lineno = models.PositiveIntegerField(_('Lineno'), db_index=True)

    class Meta:
        ordering = ['-timestamp']
        unique_together = ('filename', 'lineno')

    def __unicode__(self):
        """Displays what appears in the log"""
        if self.event_type in self.TYPES_SUBST:
            template = u'%%s %s %%s %%s' % self.TYPES_SUBST[self.event_type]
        elif self.event_type == self.ME:
            template = u'%s * %s %s'
        elif self.event_type in (self.NICK, self.MODE):
            template = u'%s *** %s %s'
        else:
            template = u'%s <%s> %s'
        date = u'[%s]' % self.timestamp.strftime('%H:%M')
        return template % (date, self.nickname, self.content)


class Link(models.Model):
    event = models.ForeignKey(Event, verbose_name=_('Link'),
                              related_name='links')
    url = models.URLField(_('URL'), verify_exists=False, max_length=400)

    def __unicode__(self):
        return u'%s' % self.url

