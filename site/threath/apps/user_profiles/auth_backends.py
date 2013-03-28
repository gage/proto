from django.contrib.auth.models import User
from django.contrib.auth import backends


class UserProfileBackend(backends.ModelBackend):
    def authenticate(self, user_id=None, sys_gen_pwd=None):
        """
        Authenticate the user, by username and system generation password
        """
        try:
            user = User.objects.get(id=user_id)
            if sys_gen_pwd == user.get_profile().system_gen_password:
                return user
            else:
                return None
        except User.DoesNotExist:
            return None
