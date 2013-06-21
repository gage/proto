from django.contrib import admin
from models import SoundCloud

class SoundCloudAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'ranking', 'image_img')
    raw_id_fields = ('photo',)
    
admin.site.register(SoundCloud, SoundCloudAdmin)

