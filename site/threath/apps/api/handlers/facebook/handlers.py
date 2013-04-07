import time
import datetime
from urllib2 import HTTPError

from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

import api.errors as api_errors
from api.errors import APIException
from api.handlers.handlers import BaseHandler, BaseIndexHandler
from api.utils import process_boolean, wrap_info
from facebook.models import FacebookProfile
from facebook.facebook_api import FacebookAPI
from facebook.utils import login_fb_user, req_exchange_long_lived_access_token

from globals.utils import get_logger
from registration.models import Registration


class ConnectHandler(BaseHandler):
    allowed_methods = ('POST', 'DELETE')
    required_fields = ('access_token',)
    create_kwargs = required_fields + ('gets',)
    create_auth_exempt = True

    def create(self, request):
        access_token = request.CLEANED['access_token']
        api = FacebookAPI(access_token)

        try:
            if not api.is_authenticated():
                raise APIException(api_errors.ERROR_FACEBOOK_INVALID_TOKEN)
            access_token, expires = req_exchange_long_lived_access_token(access_token)
            api = FacebookAPI(access_token)
        except HTTPError:
            raise APIException(api_errors.ERROR_FACEBOOK_BAD_REQUEST)

        if not request.user.is_authenticated():
            user, created = api.connect()
            local_fb_profile = user.get_profile().get_fb_profile()
            user = authenticate(facebook_id=local_fb_profile.facebook_id)
            auth_login(request, user)

        user = request.user

        local_fb_profile = user.get_profile().get_fb_profile()
        if not local_fb_profile:
            local_fb_profile = api.attach_local_profile(user)
        local_fb_profile.is_active = True
        local_fb_profile.save()

        gets = request.CLEANED.get('gets', False)

        return wrap_info(user.get_profile().to_json(request, detail=True), {})

    def delete(self, request, **kwargs):
        try:
            fb_profile = request.user.fb_profile
            fb_profile.delete()
            return {}
        except FacebookProfile.DoesNotExist:
            raise APIException(api_errors.ERROR_FACEBOOK_NO_PROFILE)

