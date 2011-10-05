from django.conf.urls.defaults import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.channels_list, name='channels_list'),

    url(r'^(?P<channel>.+)/$', views.channel_detail, name='channel_detail'),

    url(r'^(?P<channel>.+)/links/$',
        views.channel_links, name='channel_links'),

    # Stats: frequency / evolution, active users, # of users
    url(r'^(?P<channel>.+)/stats/$',
        views.channel_stats, name='channel_stats'),
)
