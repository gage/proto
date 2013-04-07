import string
from random import choice

from django.contrib.auth.models import User
from django.conf import settings

from facebook.graph_api import GraphAPI, GraphAPIError
from facebook.models import FacebookProfile
from photos.threads import PhotoDownloadThread
from photos.models import Photo, get_picture_from_url


class FacebookAPIError(Exception):
    pass


class FacebookNotAuthenticated(FacebookAPIError):
    pass


class DuplicateLocalProfile(FacebookAPIError):
    pass


class FacebookAPI(GraphAPI):
    """ Facebook API wrapper """
    def __init__(self, access_token=None):
        self._is_authenticated = None
        self._profile = None
        self.access_token = access_token
        if self.access_token:
            GraphAPI.__init__(self, access_token)

    def is_authenticated(self):
        """ Checks if the cookie/post data provided is actually valid """
        if self._is_authenticated is None:
            try:
                self.get_profile()
                self._is_authenticated = True
            except GraphAPIError:
                self._is_authenticated = False
        return self._is_authenticated

    def get_profile(self):
        """ Returns user's profile data with images """
        if self._profile is None:
            profile = self.get_object('me', date_format='U')
            profile['image'] = 'https://graph.facebook.com/me/picture?type=large&access_token=%s' % self.access_token
            profile['image_thumb'] = 'https://graph.facebook.com/me/picture?access_token=%s' % self.access_token

            print "profile in facebook_api: %s" % profile

            self._profile = profile
        return self._profile

    def connect(self, username=None):
        """ Gets or creates a user associated with this facebook ID.  Also serves to
        update the user's facebook access token.

        Returns:
            User, created: User object for this access token, True or False if the User was newly
                created.
        """
        if not self.is_authenticated():
            raise FacebookNotAuthenticated("A valid access token is required.")

        created = False
        fb_profile = self.get_profile()
        local_fb_profile = self.get_local_profile()
        user = None
        # Existing user, already connected
        if local_fb_profile:
            user = local_fb_profile.user

        if not user:
            # New user, or first FB connect
            try:
                user = User.objects.get(email=fb_profile['email'])
            except User.DoesNotExist:
                user = User(username = self._generate_unique_username(fb_profile), email = fb_profile['email'] )
                user.set_password(self._generate_fake_password())
                created = True

        if not user.first_name:
            user.first_name = fb_profile['first_name']
        if not user.last_name:
            user.last_name = fb_profile['last_name']

        user.save()
        up = user.get_profile()
        if not up.full_name:
            up.full_name = fb_profile['name']
        if not up.has_set_photo():
            photo = get_picture_from_url(fb_profile['image'])
            up.main_profile_pic = photo
        up.save()

        if not local_fb_profile:
            self.create_local_profile(user)

        return user, created

    # TODO(BDH): Clean this up
    def build_user_fb_img(self, user):
        fb_profile = self.get_profile()
        photo = Photo.objects.create()
        Photo.objects.filter(pk=photo.pk).update(image='photos/img_user_fallback.png')
        user_profile = user.get_profile()
        user_profile.profile_pic = photo
        user_profile.save()
        image_url = fb_profile['image']
        obj = (image_url, photo)
        if not settings.REAL_TIME_SEARCH_INDEX:
            return
        PhotoDownloadThread.put(obj)

    def create_local_profile(self, user):
        """ Creates a new local FacebookProfile for the current auth token and returns it.

        Args:
            user: Auth User to attach this profile to.
        """
        if not self.is_authenticated():
            raise FacebookNotAuthenticated("A valid access token is required.")

        fb_profile = self.get_profile()
        try:
            local_fb_profile = FacebookProfile.objects.get(facebook_id=fb_profile['id'])
            raise DuplicateLocalProfile("Profile for id %s already exists." % fb_profile['id'])
        except FacebookProfile.DoesNotExist:
            local_fb_profile = FacebookProfile.objects.create(
                user=user,
                facebook_id=fb_profile['id'],
                access_token=self.access_token,
            )
            return local_fb_profile

    def attach_local_profile(self, user):
        """ Attach (or Create & Attach) a local FacebookProfile for the current auth token and returns it.

        Args:
            user: Auth User to attach this profile to.
        """
        if not self.is_authenticated():
            raise FacebookNotAuthenticated("A valid access token is required.")

        fb_profile = self.get_profile()

        try:
            origin_fb_profile = user.fb_profile
            origin_fb_profile.delete()
        except FacebookProfile.DoesNotExist:
            pass

        try:
            local_fb_profile = FacebookProfile.objects.get(facebook_id=fb_profile['id'])
            local_fb_profile.user = user
            local_fb_profile.save()
        except FacebookProfile.DoesNotExist:
            local_fb_profile = FacebookProfile.objects.create(
                user=user,
                facebook_id=fb_profile['id'],
                access_token=self.access_token,
            )
        return local_fb_profile

    def get_local_profile(self):
        """ Gets local FacebookProfile for the current auth token.  Returns None if
        non-existant. """
        if not self.is_authenticated():
            raise FacebookNotAuthenticated("A valid access token is required.")

        fb_profile = self.get_profile()
        try:
            # Update access_token
            local_fb_profile = FacebookProfile.objects.get(facebook_id=fb_profile['id'])
            local_fb_profile.access_token = self.access_token
            local_fb_profile.save()
            return local_fb_profile
        except FacebookProfile.DoesNotExist:
            return None

    def get_friends(self):
        if not self.is_authenticated():
            raise FacebookNotAuthenticated("A valid access token is required.")

        friends = self.get_connections(self.get_profile()['id'], "friends")
        return friends['data']

    @classmethod
    def _generate_fake_password(cls):
        """ Returns a random fake password """
        password = "".join([choice(string.letters + string.digits) for i in range(9)])
        return password.lower()

    @classmethod
    def _generate_unique_username(cls, fb_profile):
        """ Returns a unique username for this facebook profile """
        try:
            candidate = fb_profile['username']
        except KeyError:
            try:
                candidate = fb_profile['email'].split('@')[0]
            except KeyError:
                candidate = 'facebookuser'

        append = 1
        while True:
            if User.objects.filter(username=candidate).count() == 0:
                return candidate
            candidate = "%s%s" % (candidate, append)
            append += 1
