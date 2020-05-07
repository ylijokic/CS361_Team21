from django.contrib import admin

from .models import Advertisement, Instrument, Location, Musician

admin.site.register(Advertisement)
admin.site.register(Instrument)
admin.site.register(Location)
admin.site.register(Musician)