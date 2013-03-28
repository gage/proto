from hashlib import sha256
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django import forms
from django.conf import settings
from user_profiles.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'full_name', )
	raw_id_fields = ('user', 'main_profile_pic', )
	search_fields = ['username']
	list_per_page = 100

admin.site.register(UserProfile, UserProfileAdmin)


class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'is_active',
                  'is_staff', 'is_superuser', 'last_login', 'date_joined', )

class CustomUserAdmin(UserAdmin):
	fieldsets = None
	form = UserForm
	list_filter = ()
	ordering = ('-date_joined', )
	search_fields = ('username', 'email')
	list_display = ('username', 'is_active', 'is_staff', 'email', 'first_name', 'last_name', 'last_login', 'date_joined', )
	
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

