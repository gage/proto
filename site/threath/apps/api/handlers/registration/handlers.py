import re

from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.validators import email_re
from django.utils.translation import ugettext as _

import api.errors as api_errors
from api.handlers.handlers import BaseHandler, BaseObjectHandler
from api.errors import APIException
from api.utils import process_boolean, process_integer, wrap_info
from registration.models import Registration, PhoneRegistration
from registration.utils import check_username, sign_up
from slug.models import Slug
from user_profiles.models import UserProfile
from user_profiles.forms import UserInfoForm, LoginForm
from photos.models import Photo
from facebook.models import FacebookProfile
from globals.auth_backends import general_login


USERNAME_FORMAT = re.compile('^[\.\w-]{5,15}$')
FULLNAME_FORMAT = re.compile('^[ \.\w-]{1,60}$')
PASSWORD_FORMAT = re.compile('^[\w\d@#\$%]{6,20}$')


def validate_username(username):
    if username.startswith('_'):
        raise api_errors.APIException(api_errors.ERROR_REGISTRATION_INVALID_USERNAME)
    #Check if the username format is valid
    if not username or not USERNAME_FORMAT.match(username):
        raise api_errors.APIException(api_errors.ERROR_REGISTRATION_INVALID_USERNAME)

    if " " in username or "-" in username:
        raise api_errors.APIException(api_errors.ERROR_REGISTRATION_INVALID_USERNAME)

    #Check if the username is available
    if not check_username(username):
        raise api_errors.APIException(api_errors.ERROR_REGISTRATION_USERNAME_UNAVAILABLE)
    return True


def validate_fullname(fullname):
    #Check if the fullname format is valid
    if not fullname or not FULLNAME_FORMAT.match(fullname):
        raise api_errors.APIException(api_errors.ERROR_REGISTRATION_INVALID_FULLNAME)
    return True


def validate_email(email, exclude_user=None, exclude_inactive=False):
    #Check if the email format is valid
    if not email or not email_re.match(email):
        raise api_errors.APIException(api_errors.ERROR_REGISTRATION_INVALID_EMAIL)

    #Check if the email is available
    params={
        'email': email,
        'exclude_inactive': exclude_inactive,
    }
    if exclude_user:
        params['exclude_user'] = exclude_user
    is_used = UserProfile.objects.check_if_email_has_been_used(**params)
    if is_used:
        raise api_errors.APIException(api_errors.ERROR_REGISTRATION_EMAIL_USED)

    return True


def validate_password(password):
    if not PASSWORD_FORMAT.match(password):
        raise api_errors.APIException(api_errors.ERROR_AUTH_PASSWORD_INVALID)

    return True


def validate_passwords(password, password_confirm):
    if password and password_confirm:
        if password != password_confirm:
            raise api_errors.APIException(api_errors.ERROR_AUTH_PASSWORD_CONFIRM_NOT_MATCH)
    if not PASSWORD_FORMAT.match(password):
        raise api_errors.APIException(api_errors.ERROR_AUTH_PASSWORD_INVALID)
    if not PASSWORD_FORMAT.match(password_confirm):
        raise api_errors.APIException(api_errors.ERROR_AUTH_PASSWORD_CONFIRM_INVALID)

    return True


# === Checked ===
class CheckUsernameHandler(BaseHandler):
    read_kwargs = ('username',)
    allowed_methods = ('GET', )
    read_auth_exempt = True

    def read_validate(self, query_dict, request, **kwargs):
        username = query_dict.get('username')
        validate_username(username)

    def read(self, request, **kwargs):
        return {}


# === Checked ===
class CheckFullnameHandler(BaseHandler):
    read_kwargs = ('fullname',)
    allowed_methods = ('GET', )
    read_auth_exempt = True

    def read_validate(self, query_dict, request, **kwargs):
        fullname = query_dict.get('fullname')
        validate_fullname(fullname)

    def read(self, request, **kwargs):
        return {}


# === Checked ===
class CheckEmailHandler(BaseHandler):
    read_kwargs = ('email', )
    allowed_methods = ('GET', )
    read_auth_exempt = True

    def read_validate(self, query_dict, request, **kwargs):
        email = query_dict.get('email')
        user = request.session.get('user', None)
        validate_email(email, exclude_user = user)

    def read(self, request, **kwargs):
        return {}


# === Checked ===
class CheckPasswordHandler(BaseHandler):
    read_kwargs = ('password', )
    allowed_methods = ('GET', )
    read_auth_exempt = True

    def read_validate(self, query_dict, request, **kwargs):
        validate_password(query_dict.get('password', ''))

    def read(self, request, **kwargs):
        return {}


# === Checked ===
class SignupHandler(BaseHandler):
    required_fields = ('fullname', 'email', 'password')
    create_kwargs = required_fields + ('username',)
    create_auth_exempt = True

    def create_validate(self, query_dict, request, **kwargs):
        if request.user.is_authenticated():
            raise api_errors.APIException(api_errors.ERROR_AUTH_USER_ALREADY_LOGIN)
        if not query_dict['username']:
            # Auto generate username
            query_dict['username'] = email.split('@')[0]
        else:
            validate_username(query_dict['username'])
        validate_email(query_dict['email'])
        validate_password(query_dict['password'])
        

    def create(self, request, **kwargs):
        """ Registers a new user and returns their user id. """
        fullname = request.CLEANED['fullname'] #this is full name actually
        email = request.CLEANED['email']
        password = request.CLEANED['password']
        username = request.CLEANED['username']

        slug_name = Slug.objects.sluggify(username)
        user = sign_up(slug_name, password, request)
        user.email = email
        user.save()
        user_profile = user.get_profile()
        user_profile.full_name = fullname
        user_profile.save()

        registration = Registration.objects.get(user=user)
        registration.send_activation_mail()
        login_method = 'normal'

        rtn = {
            'user_id': user.pk,
            "login_method": login_method,
            "status": registration.status,
        }
        return rtn


# === Checked ===
class SendForgetPasswordEmailHandler(BaseHandler):
    allowed_methods = ('POST', )
    required_fields = ('username',)
    create_auth_exempt = True

    def create_validate(self, query_dict, request, **kwargs):
        username =  query_dict.get('username').lower()
        try:
            user = User.objects.get(username__iexact=username)
        except:
            raise APIException(api_errors.ERROR_REGISTRATION_INVALID_USERNAME)
        query_dict['user'] = user

    def create(self, request, **kwargs):
        user = request.CLEANED.get('user')
        try:
            registration = Registration.objects.get(user=user)
            registration.gen_activation_code()
        except Registration.DoesNotExist:
            registration = Registration.objects.create_registration_obj_for_user(user = user)
            registration.gen_activation_code()
        registration.send_forget_password_mail()
        return {}


# === Checked ===
class ResendAccountActivationCodeHandler(BaseHandler):
    allowed_methods = ('POST', )
    required_fields = ('email',)
    create_auth_exempt = True

    def create_validate(self, query_dict, request, **kwargs):
        email = query_dict['email']
        user = User.objects.get(email=email)
        query_dict['user'] = user

    def create(self, request, **kwargs):
        user = request.CLEANED['user']
        if user:
            registration = Registration.objects.get(user=user)
            registration.send_activation_mail()
        else:
            raise APIException(api_errors.ERROR_AUTH_BAD_CREDENTIALS)
        return {}


class ActivateHandler(BaseHandler):
    allowed_methods = ('POST',)
    required_fields = ('activation_code',)
    create_auth_exempt = True

    def create_validate(self, query_dict, request, **kwargs):
        if request.user.is_active:
            raise APIException(api_errors.ERROR_AUTH_USER_ALREADY_ACTIVATED)

    def create(self, request, **kwargs):
        registration = Registration.objects.activate(request, request.CLEANED['activation_code'], mobile=True)
        if registration:
            user = registration.user
            up = user.get_profile()
            rtn = {
                "status": registration.status,
                "login_method": "activation",
                "user_id": user.id,
                "username": user.username,
                "is_first_login": up.is_first_login,
                "is_first_login_mobile": up.is_first_login_mobile,
            }
            return rtn
        else:
            return False
