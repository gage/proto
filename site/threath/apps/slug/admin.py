from django.contrib import admin
from slug.models import Slug

class SlugAdmin(admin.ModelAdmin):
    #list_display = ('pk', 'name', 'category', 'address', 'city', 'state', 'created', 'is_featured')
    search_fields = ['name']
    #raw_id_fields = ('main_profile_pic',)

admin.site.register(Slug, SlugAdmin)

