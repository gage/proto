from django.contrib.auth import authenticate, login, logout
from django.core.validators import email_re
from django.contrib.auth.models import User
from django.conf import settings

from globals.auth_backends import general_login
from globals.utils import is_mongo_pk
import api.errors as api_errors
from api.handlers.handlers import BaseHandler
from api.utils import wrap_info

from user_profiles.models import UserProfile
from registration.models import Registration


# ============== Operation Handler =============
class LogoutHandler(BaseHandler):
    def create(self, request):
        UserProfile.objects.filter(user=request.user).update(iphone_device_token="")
        logout(request)
        return


# === Checked ===
class GeneralSigninHandler(BaseHandler):
    required_fields = ('password', )
    create_kwargs = required_fields + ('user_identity', 'username')
    create_auth_exempt = True

    def create_validate(self, query_dict, **kwargs):
        # user_identity can be email, username, user_id, phone_sms_e164
        if query_dict.get('username'):
            user_identity = query_dict.get('username')
        else:
            user_identity = query_dict.get('user_identity')
        try:
            if is_mongo_pk(user_identity):
                user = User.objects.get(id=user_identity)
                query_dict['use_system_gen_password'] = True
            elif user_identity.startswith('+'):
                user_profile = UserProfile.objects.get(phone_sms_e164=user_identity)
                user = user_profile.user
            elif email_re.match(user_identity):
                user = User.objects.get(email=user_identity)
            else:
                user = User.objects.get(username=user_identity)
        except User.DoesNotExist:
            raise api_errors.APIException(api_errors.ERROR_AUTH_USERNAME_NOT_EXIST)

        if not user.is_active:
            raise api_errors.APIException(api_errors.ERROR_REGISTRATION_NOT_ACTIVATE)

        query_dict['user'] = user

    def create(self, request):
        user = request.CLEANED['user']
        password = request.CLEANED['password']
        use_system_gen_password = request.CLEANED.get('use_system_gen_password')

        # Phone Device, Desktop Auto login
        if use_system_gen_password:
            auth_user = authenticate(user_id=user.id, sys_gen_pwd=password)
        else:
            auth_user = authenticate(username=user.username, password=password)

        if not auth_user:
            raise api_errors.APIException(api_errors.ERROR_USER_PASSWORD_NOT_MATCH)
        general_login(request, auth_user)
        return auth_user.to_json(request=request, detail=True)
    