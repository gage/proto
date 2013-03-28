__author__ = ""

from datetime import datetime
from haystack.query import SearchQuerySet
import time

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.core.validators import email_re
from django.core.mail import mail_admins
from django.utils.translation import ugettext as _

from api.handlers.handlers import BaseIndexHandler, BaseObjectHandler, BaseHandler, BaseSearchHandler
from api.errors import APIException
from api.utils import process_boolean, wrap_info
import api.errors as api_errors

from photos.models import Photo
from user_profiles.models import UserProfile
from user_profiles.forms import UserSettingsForm
# from friend_list.models import FriendList

from django.conf import settings


class IndexHandler(BaseIndexHandler):
    allowed_methods = ('GET', )
    query_model = User
    read_auth_exempt = True

    def read_validate(self, query_dict, request):
        query_dict['custom_query'] = User.objects.all().exclude(username='AnonymousUser')


class ObjectHandler(BaseObjectHandler):
    allowed_methods = ('GET', )
    query_model = User
    read_auth_exempt = True


# ============== Search Handler =============
class SearchHandler(BaseSearchHandler):
    allowed_methods = ('GET',)
    allowed_filter = ('name', 'email', 'full_name')
    query_model = User

    def read(self, request):
        results = super(SearchHandler, self).read(request)
        return [p.object.to_json(request=request, detail=request.CLEANED['detail']) for p in results]


class MeHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        if not request.user.is_authenticated():
            raise APIException(api_errors.ERROR_AUTH_NOT_AUTHENTICATED)
        url = request.path.replace('/me', '/%s' % request.user.id)
        return redirect(url)



# # ============== Search Friend Handler =============
# class SearchFriendHandler(BaseSearchHandler):
#     allowed_methods = ('GET',)
#     allowed_filter = ('name', 'email', 'full_name')
#     query_model = User

#     def read_validate(self, query_dict, request, **kwargs):
#         super(SearchFriendHandler, self).read_validate(query_dict, request=request)
#         friends_id = Group.objects.get_user_friends_search_id(request.user)
#         friends_id.append('auth.user.' + request.user.id)
#         query_dict['custom_query'] = SearchQuerySet().models(User).exclude(id__in=friends_id)
#         query_dict['filter_type'] = 'startswith'

#     def read(self, request):
#         results = super(SearchFriendHandler, self).read(request)

#         sent_request = FriendList.objects.get_user_sent_requests(request.user)
#         reveive_request = FriendList.objects.get_user_receive_requests(request.user)

#         rtn = []
#         for p in results:
#             try:
#                 json = p.object.to_json(request=request, detail=request.CLEANED['detail'])

#                 if p.object.id in [req.user.pk for req in sent_request]:
#                     json['friend_req_status'] = 2 #request sent
#                 elif p.object.id in [req.user.pk for req in reveive_request]:
#                     json['friend_req_status'] = 1 #request received
#                 else:
#                     json['friend_req_status'] = 0 #no request yet
#                 rtn.append(json)
#             except AttributeError as e:
#                 print e

#         return rtn


# # ============== Operation Handler =============
# class FriendHandler(BaseHandler):
#     """Do friend request (POST), response friend request (POST)"""
#     allowed_methods = ('POST',)
#     create_kwargs = ('title', 'msg')

#     def create_validate(self, query_dict, request, object_id, **kwargs):
#         if object_id == request.user.id:
#             raise APIException(api_errors.ERROR_GENERAL_INVALID_OPERATION)

#     def create(self, request, object_id):
#         title = request.CLEANED['title']
#         msg = request.CLEANED['msg']

#         sender = User.objects.get(id=request.user.id)
#         receiver = User.objects.get(id=object_id)
#         status = FriendList.objects.make_user_friend_request(sender, receiver, title=title, msg=msg)
#         return {'status': status}
