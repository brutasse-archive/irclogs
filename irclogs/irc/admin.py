from django.contrib import admin

from .models import Channel, Event


class ChannelAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    list_filter = ('channel', 'timestamp', 'event_type', 'nickname',)
    search_fields = ['content']

admin.site.register(Channel, ChannelAdmin)
admin.site.register(Event, EventAdmin)
