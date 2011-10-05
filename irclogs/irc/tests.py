from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Event, Channel


class IRCTest(TestCase):
    def test_channels_list(self):
        url = reverse('channels_list')
        response = self.client.get(url)
        self.assertContains(response, 'Channels')
