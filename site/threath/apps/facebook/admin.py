from django.contrib import admin

from facebook.models import FacebookProfile


class FacebookProfileAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'facebook_id')
    raw_id_fields = ['user']

admin.site.register(FacebookProfile, FacebookProfileAdmin)