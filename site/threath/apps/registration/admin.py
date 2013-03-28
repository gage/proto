""" Registration admin configuration """

from django.contrib import admin

from registration.models import Registration
from registration.models import PhoneRegistration


class PhoneRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created')
    raw_id_fields = ('user', )

admin.site.register(Registration)
admin.site.register(PhoneRegistration, PhoneRegistrationAdmin)
