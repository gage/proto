from django.contrib import admin
from place.models import FoursquarePlace

class FoursquarePlaceAdmin(admin.ModelAdmin):
    fields = ('fid', 'name', 'address',)
    
admin.site.register(FoursquarePlace, FoursquarePlaceAdmin)

