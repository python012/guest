from django.contrib import admin
from sign.models import Event
from sign.models import Guest


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'address', 'start_time']


class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone', 'email', 'sign', 'create_time', 'event']


# Register your models here.
admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
