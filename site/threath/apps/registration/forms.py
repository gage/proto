import re

from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from registration.utils import check_username

class SignupForm(forms.ModelForm):
    """ User signup form """
    
    is_resend = False
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class':'txt'}))
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'class':'txt'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class':'txt'}))
    
    class Meta:
        model = User
        fields = (
            'username',
            'email', 
            'password',
            'password_confirm',
        )
        widgets = {
            'email': forms.TextInput(attrs={'class':'txt'}),
        }

    def clean(self):
        data = self.cleaned_data
        username = data.get('username')
        
        if not self.is_resend and 'username' in data:
            if check_username(username) is False:
                msg = _("This username is not available or already in use.")
                self._errors["username"] = self.error_class([msg])
                del data["username"]

        return data
    
    def clean_username(self):
        """ Ensure username is a valid slug and available """
        username = self.cleaned_data['username']
        rule = re.compile('^[\w-]+$')
        try:
            rule.match(username).group()
        except:
            raise forms.ValidationError(_("Enter a valid username consisting of letters, numbers, underscores or hyphens."))
            
        return username
    
    def clean_email(self):
        """ Ensure email is unique """
        email = self.cleaned_data['email']
        if email != '':
            if User.objects.filter(email__iexact=email).count() > 0:
                user = User.objects.get(email__iexact=email)
                if user.is_active or user.get_profile().is_slave:
                    raise forms.ValidationError(_("This email address is already in use."))
                else:
                    self.is_resend = True
            
        else:
            raise forms.ValidationError(_("This field is required."))
        
        return email.lower()
    
    def clean_password_confirm(self):
        data = self.cleaned_data
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        
        if password and password != password_confirm:
            raise forms.ValidationError(_("Passwords don't match."))
        return data
        
        
        
class ResetPasswordForm(forms.ModelForm):
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(attrs={'class':'txt'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class':'txt'}))
    
    class Meta:
        model = User
        fields = (
            'password',
            'password_confirm',
        )
        
    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password and password != password_confirm:
            raise forms.ValidationError(_("Passwords don't match."))
        return data
    