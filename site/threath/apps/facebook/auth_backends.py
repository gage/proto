from django.contrib.auth import backends

from facebook.models import FacebookProfile

class FacebookBackend(backends.ModelBackend):
    def authenticate(self, facebook_id=None):
        """
        Authenticate the facebook user by facebook_id
        """        
        try:
            fb_profile = FacebookProfile.objects.get(facebook_id=facebook_id)
            return fb_profile.user
        except FacebookProfile.DoesNotExist:
            return None
