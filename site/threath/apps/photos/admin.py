""" Photos admin configuration """

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.forms import widgets
from django.db import models
from imagekit.admin import AdminThumbnail

from photos.models import *

class GenericPhotoInline(generic.GenericTabularInline):
    model = Photo
    #fields = []


class PhotoAdmin(admin.ModelAdmin):
    """ Base photo admin class """
    list_display = ('pk', 'title', 'user', 'object_id', 'created', 'admin_thumbnail')

    list_filter = ['all_default', 'user_default', 'created', 'album_default']

    list_per_page = 10
    raw_id_fields = ('user',)
    admin_thumbnail = AdminThumbnail(image_field='image50x50')

admin.site.register(Photo, PhotoAdmin)
