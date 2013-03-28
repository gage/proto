import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.validators import email_re

#from globals.timezones import TIMEZONE_CHOICES
#from globals.languages import LANGUAGE_CHOICES
from user_profiles.models import UserProfile
from photos.models import Photo
from registration.utils import check_username


def validate_full_name(test_string, field_name="", error_msg=None):
    if not re.search(r"^[ \w\d-]{0,60}$", test_string):
        if error_msg:
            raise forms.ValidationError(_(error_msg))
        else:
            if field_name:
                field_name = "The field %s" % field_name
            else:
                field_name = "This field"
            raise forms.ValidationError(_("%s must contain letters or numbers, between 1 and 60 characters." % field_name))


def validate_alphanumeric_only(test_string, field_name="", error_msg=None):
    if not re.search(r"^[\w\d-]+$", test_string):
        if error_msg:
            raise forms.ValidationError(_(error_msg))
        else:
            if field_name:
                field_name = "The field %s" % field_name
            else:
                field_name = "This field"
            raise forms.ValidationError(_("%s can only contain alphanumeric characters." % field_name))

def validate_non_empty_string(test_string, field_name="", error_msg=None):
    if not test_string :
        if error_msg:
            raise forms.ValidationError(_(error_msg))
        else:
            if field_name:
                field_name = "The field %s" % field_name
            else:
                field_name = "This field"
            raise forms.ValidationError(_("%s is required." % field_name))


class UserInfoForm(forms.Form):
    full_name = forms.CharField(required=False, max_length=60)
    photo_id = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'class':'photo_id'}))
    birthday = forms.DateField(required=False, )
    gender = forms.ChoiceField(required=False, choices=UserProfile.GENDER_CHOICES)
    
    primary_email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.check_primary_email = kwargs.pop('check_primary_email', None)
        self.exclude_user = kwargs.pop('exclude_user', None)
        
        super(forms.Form, self).__init__(*args, **kwargs)

    def clean_primary_email(self):
        cleaned_data = self.cleaned_data
        primary_email = cleaned_data['primary_email']
        
        if self.check_primary_email:
            validate_non_empty_string(primary_email, field_name='primary email')
        
            if primary_email:
                if UserProfile.objects.check_if_email_has_been_used(primary_email, self.exclude_user):
                    raise forms.ValidationError(_("The email %s has been used." % primary_email))
            
        return primary_email

    def clean_full_name(self):
        cleaned_data = self.cleaned_data
        full_name = cleaned_data.get('full_name')
        
        validate_full_name(full_name, field_name='full name')
        return full_name

    def clean_photo_id(self):
        cleaned_data = self.cleaned_data
        photo_id = cleaned_data['photo_id']
        
        if photo_id == "":
            return 
                
        try:
            Photo.objects.get(id=photo_id)
        except:
            raise forms.ValidationError(_("Photo id is invalid."))
        
        return photo_id

    def clean_birthday(self):
        cleaned_data = self.cleaned_data
        birthday = cleaned_data['birthday']

        validate_non_empty_string(birthday, field_name='birthday')
        return birthday

    def clean_gender(self):
        cleaned_data = self.cleaned_data
        gender = cleaned_data['gender']

        validate_non_empty_string(gender, field_name='gender')
        return gender


class LoginForm(forms.Form):
    username = forms.CharField(required=False, min_length=5, max_length=15)
    password = forms.CharField(required=False, min_length=6, max_length=20, widget=forms.PasswordInput(attrs={'class':'txt', 'size':'48'}))
    password_confirm = forms.CharField(required=False, min_length=6, max_length=20, widget=forms.PasswordInput(attrs={'class':'txt', 'size':'48'}))

    def __init__(self, *args, **kwargs):
        self.user_in_session = kwargs.pop('user_in_session', None)
        super(forms.Form, self).__init__(*args, **kwargs)

    def clean_username(self):
        cleaned_data = self.cleaned_data
        
        """ Ensure username is a valid slug and available """
        username = cleaned_data.get('username')
        user = self.user_in_session
        
        if not check_username(username):
            if user:
                exist_usernames = User.objects.filter(username=username).exclude(id=user.id)
                # Check if username is available
                if exist_usernames:
                    raise forms.ValidationError(_("This username has already been used by another user."))
            else:
                raise forms.ValidationError(_("This username is not available."))
        
        validate_non_empty_string(username, field_name='username')
        validate_alphanumeric_only(username, field_name='username')
        
        return username

    def clean_password(self):
        cleaned_data = self.cleaned_data

        password = cleaned_data.get('password')
        validate_non_empty_string(password, field_name='password')
    
        return password


    def clean_password_confirm(self):
        cleaned_data = self.cleaned_data

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        validate_non_empty_string(password_confirm, field_name='confirmation password')
        
        if password:
            if password != password_confirm:
                raise forms.ValidationError(_("Passwords do not match."))
        return password_confirm
        


class UserSettingsForm(UserInfoForm):
    is_change_password = False
    
    username = forms.CharField(required=True, min_length=5, max_length=15)
    password_old = forms.CharField(required=False, min_length=6, max_length=20, widget=forms.PasswordInput(attrs={'class':'txt', 'size':'48'}))
    password_new = forms.CharField(required=False, min_length=6, max_length=20, widget=forms.PasswordInput(attrs={'class':'txt', 'size':'48'}))
    password_confirm = forms.CharField(required=False, min_length=6, max_length=20, widget=forms.PasswordInput(attrs={'class':'txt', 'size':'48'}))

    #timezone = forms.ChoiceField(required=True, choices=TIMEZONE_CHOICES)
    #language = forms.ChoiceField(required=True, choices=LANGUAGE_CHOICES)
        
    def __init__(self, *args, **kwargs):
        
        UserInfoForm.__init__(self, *args, **kwargs)
        #super(UserInfoForm, self).__init__(*args, **kwargs)
    
#    def clean(self):
#        cleaned_data = self.cleaned_data
#        return cleaned_data
            
    def clean_username(self):
        cleaned_data = self.cleaned_data
        
        """ Ensure username is a valid slug and available """
        username = cleaned_data.get('username')
        username = username.lower()
        user = self.request.user
        
        if user.username != username:
            #valid using slug validate
            # valid = Slug.objects.validate(username)
            
            if not valid:
                raise forms.ValidationError(_("This username is not valid")) 
        return username
    
    def clean_password_old(self):
        
        '''
        Check if this field has value
        if yes, 
            verify if this matches the user
            if yes,
                store a token that can notify the following two fields to enter the change password process
            no
               raise password mismatch error
        no
            store a token that can notify the form to ommit the following two fields
        '''

        cleaned_data = self.cleaned_data

        username = cleaned_data.get('username')
        password_old = cleaned_data.get('password_old')

        #validate_non_empty_string(password_old)

        #print "username: %s" % username
        #print "password_old: %s" % password_old
        
        if password_old:
            if not authenticate(username=self.request.user.username, password=password_old):
                raise forms.ValidationError(_("Password is incorrect."))
        
        return password_old
    
    def clean_password_new(self):
        cleaned_data = self.cleaned_data

        password_new = cleaned_data.get('password_new')
        #validate_non_empty_string(password_new)
    
        return password_new
    
    def clean_password_confirm(self):
        cleaned_data = self.cleaned_data

        password_new = cleaned_data.get('password_new')
        password_confirm = cleaned_data.get('password_confirm')
        
        #validate_non_empty_string(password_confirm)
        
        if password_new:
            if password_new != password_confirm:
                raise forms.ValidationError(_("New password and new password confirm don't match."))
        return password_confirm
