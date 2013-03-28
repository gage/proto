import datetime
import re
import urlparse
import uuid

from django.db.models.loading import get_model
from django.conf import settings
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponsePermanentRedirect
from django.http import Http404, HttpResponseRedirect, get_host
from django.shortcuts import render_to_response
from django.template import RequestContext

from slug.models import Slug
from django.contrib.contenttypes.models import ContentType

MONGO_PK = re.compile(r'[a-fA-F0-9]{24}')
URL_IGNORE = ['media', 'static', 'islogin', 'monitor', 'contact', 'my_admin']
URL_API = 'api'


class SlugURLMiddleware(object):
    """
    Translates slug-prefixed URLs (currently for users only) into their expanded
    form and redirects expanded URLs into their slug-prefixed form where
    appropriate.
    """
    def _to_slug(self, request):
        if request.is_ajax() or request.method == "POST":
            return

        path = request.path.split('/')
        parsed_path = urlparse.urlparse(request.get_full_path())

        try:
            user = User.objects.get(pk=path[2])
            redirect_url = urlparse.urlunparse((None, None, "/%s/%s" % (user.username, "/".join(path[3:])),
                None, parsed_path.query, None))
            return HttpResponsePermanentRedirect(redirect_url)
        except User.DoesNotExist:
            return Http404

    def _from_slug(self, request):
        path = request.path.split('/')
        parsed_path = urlparse.urlparse(request.get_full_path())
        try:
            #user = User.objects.get(username=path[1])

            slug = Slug.objects.get(slug=path[1])
            obj = slug.content_object
            type = slug.content_type
        
            sub_path = 'user'
                
            request.path_info = "/%s/%s/%s" % (sub_path, obj.pk, "/".join(path[2:]))

        except Slug.DoesNotExist:
            pass
        return

    def process_request(self, request):
        path = request.path.split('/')

        # Ignore root URL
        if not path[1]:
            return

        # URLs of the form /user/<mongo pk>/... should be hard-redirected
        # to their slug-prefixed equivalent
        if path[1] in URL_MODEL_MAPPINGS and len(path) > 2 and MONGO_PK.match(path[2]):
            return self._to_slug(request)

        # URLs which are slug-prefixed need to have the expanded URL set
        # on the request object
        if path[1] not in settings.SLUG_RESTRICTED_KEYWORDS:
            return self._from_slug(request)

URL_MODEL_MAPPINGS = {
    'user': 'auth.User',
}

class ContentObjectMiddleware(object):
    """
    Attempts to populate request.content_object from URLs prefixed using
    the form /<content_type>/<pk>/.  Content types in URLs are mapped to
    django models in URL_MODEL_MAPPINGS.

    The exception to this is users which have their corresponding UserProfile
    attached instead.
    """

    def _get_model(self, type):
        try:
            path = URL_MODEL_MAPPINGS[type].split('.')
            return get_model(path[0], path[1])
        except KeyError:
            return None

    def _get_object(self, type, pk):
        model = self._get_model(type)
        if not model or not MONGO_PK.match(pk):
            return None

        try:
            return model.objects.get(pk=pk)
        except model.DoesNotExist:
            return None

    def process_request(self, request):
        request.content_object = None
        url_info = request.path_info.split('/')
        if len(url_info) < 3:
            return

        content_object = self._get_object(url_info[1], url_info[2])

        # Exception for users, attach UserProfile instead
        if url_info[1] == 'user' and content_object:
            content_object = content_object.get_profile()

        request.content_object = content_object


class MobileDetectMiddleware(object):
    """
    Attempt to detect mobile browsers.

    A better implementation would probably be based on
    http://wurfl.sourceforge.net/
    or
    http://www.zytrax.com/tech/web/mobile_ids.html
    """

    mobileRE = re.compile(r'android|fennec|iemobile|iphone|ipad|opera (?:mini|mobi)', re.IGNORECASE)
    androidRE = re.compile(r'android|fennec|iemobile|opera (?:mini|mobi)', re.IGNORECASE)

    def process_request(self, request):
        path = request.path.split('/')
        if path[1] in URL_IGNORE:
            return
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if 'MSIE 6' in user_agent:
            return render_to_response('ienotsupport.html', context_instance = RequestContext(request))

        request.mobile_browser = bool(self.mobileRE.search(request.META.get('HTTP_USER_AGENT', '')))
        request.is_android = bool(self.androidRE.search(request.META.get('HTTP_USER_AGENT', '')))


class PrivacyMiddleware(object):
    """
    Raise 404 page if the request user don't have permission to see the request result
    """
    def process_request(self, request):
        path = request.path.split('/')
        if path[1] in URL_IGNORE:
            return
        if request.user.is_authenticated() and request.user.get_profile().is_slave:
            logout(request)
        request.viewable = True
        if request.content_object.__class__.__name__ == 'UserProfile':
            user_profile = request.content_object
            if request.user.id in request.content_object.block_user_set:
                raise Http404
            if not user_profile.viewable_by(request.user):
                if request.content_object.get_privacy() == 'private':
                    raise Http404
                else:
                    request.viewable = False



class TranslateMiddleware(object):
    def process_response(self, request, response):
        path = request.path.split('/')
        if path[1] in URL_IGNORE:
            return response
        try:
            user_profile = request.user.get_profile()
        except:
            user_profile = None

        if user_profile:
            if user_profile.accept_language:
                request.session['django_language'] = user_profile.accept_language.split(",")[0].lower()
        else:
            pass

        return response


class LoginCookieMiddleware(object):
    def process_response(self, request, response):
        if not request.COOKIES.get('browserid', None):
            response.set_cookie('browserid', unicode(uuid.uuid4()))
        path = request.path.split('/')
        if path[1] in URL_IGNORE:
            return response
        if request.user.is_authenticated():
            response.set_cookie('_sitein', unicode(uuid.uuid4()))
            response.delete_cookie('_siteout')
        else:
            response.set_cookie('_siteout', unicode(uuid.uuid4()))
            response.delete_cookie('_sitein')
        return response



