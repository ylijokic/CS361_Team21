from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Advertisement, Instrument, Location, Musician


class MusicianInline(admin.TabularInline):
    model = Musician
    can_delete = False
    verbose_name_plural = 'musician'


class UserAdmin(BaseUserAdmin):
    inlines = (MusicianInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Advertisement)
admin.site.register(Instrument)
admin.site.register(Location)