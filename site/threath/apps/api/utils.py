import time
from collections import namedtuple

from datetime import datetime
from django.utils import simplejson
from django.db.models import get_model
from django.contrib.auth.models import User
from django.http import QueryDict

import api.errors as api_errors
from api.errors import APIException

# New api django_ct
TYPE_LIST = ['Unknown', 'auth.user', 'chat.chat', 'comments.comment', 'dare.dare', 'dish.dish',
             'events.event', 'place.place', 'photos.photo', 'post.post', 'review.review', 'wantto.wantto', 'tests.testmodel',
             'tests.likabletestmodel', 'group.group', 'social_stream.socialstream', 'file_sharing.sharefile', 'events.eventpost', 'xmppchat.reply']

EARTH_RADIUS = 6378.0 #km

APP_LIST = ('wantto', 'dare')

TOKEN_LENGTH = 20
DEFAULT_RETURN_NUM = 20
MAX_RETURN_NUM = 300

SysRequest = namedtuple('SysRequest', ['user', 'CLEANED'])

def create_sys_request(user, query_dict=None):
    if not query_dict:
        query_dict = QueryDict('', mutable=True)
        query_dict['detail'] = True
        query_dict['offset'], query_dict['limit'] = parse_pagination()
        query_dict['endpoint'] = query_dict['offset'] + query_dict['limit']
        query_dict['order_by'] = None
        
    sys_request = SysRequest(user=user, CLEANED=query_dict)
    return sys_request

def get_target_object(target_type, target_id):
    django_ct = target_type

    if django_ct not in TYPE_LIST:
        raise APIException(api_errors.ERROR_GENERAL_BAD_TYPE, 'Content Type Not Found for %s' % target_type)

    django_ct_args = django_ct.split('.')
    klass = get_model(*django_ct_args)
    target = klass.objects.get(id=target_id)
    return target


def to_json(obj, **kwargs):
    obj = obj.get_profile() if obj.__class__ == User else obj
    return obj.to_json(**kwargs) if hasattr(obj, 'to_json') else obj


def process_timestamp(query_dict, process_fields=[]):
    try:
        for field in process_fields:
            if query_dict.get(field) != None:
                query_dict[field] = datetime.fromtimestamp(float(query_dict[field]))
    except:
        raise APIException(api_errors.ERROR_GENERAL_BAD_PARA_FORMAT, 'Not valid timestamp format.')


def process_latlon(latlon):
    if not latlon:
        raise APIException(api_errors.ERROR_GENERAL_BAD_SIGNATURE, 'Location information is missing.')

    latlon_list = latlon.split(',')
    if len(latlon_list) != 2:
        raise APIException(api_errors.ERROR_GENERAL_BAD_PARA_FORMAT, 'Location format is not valid.')

    try:
        latitude, longitude = map(lambda x:float(x), latlon_list)
    except (TypeError, KeyError):
        raise APIException(api_errors.ERROR_GENERAL_BAD_PARA_FORMAT, 'Location format is not valid.')

    if -90>latitude or latitude>90:
        raise APIException(api_errors.ERROR_GENERAL_BAD_PARA_FORMAT, 'latitude is out of range. It should be in [-90,90], and it is %s.'% latitude)

    if -180>longitude or longitude>180:
        raise APIException(api_errors.ERROR_GENERAL_BAD_PARA_FORMAT, 'longitude is out of range. It should be in [-180,180], and it is %s.'% longitude)

    return (latitude, longitude)


def process_boolean(query_dict, process_fields=[]):
    # boolean is 'true', 'false' or None and will transform into True, False and None
    for field in process_fields:
        if query_dict.get(field) != None:
            query_dict[field] = query_dict[field] in ('true', 'True', '1', True, 1)


def process_list(query_dict, process_fields=[]):
    # This should only used for POST function
    for field in process_fields:
        if query_dict.get(field) not in (None, ''):
            query_dict[field] = query_dict[field].split(',')
        else:
            query_dict[field] = []

def process_float(query_dict, process_fields=[]):

    for field in process_fields:
        if query_dict.get(field) != None:
            if not query_dict[field]: #empty string
                query_dict[field] = None
            else:
                try:
                    query_dict[field] = float(query_dict[field])
                except:
                    raise APIException(api_errors.ERROR_GENERAL_BAD_PARA_FORMAT, 'Not valid float format.')

def process_integer(query_dict, process_fields=[]):
    try:
        for field in process_fields:
            if query_dict.get(field)!=None:
                query_dict[field] = int(query_dict[field].split('.')[0])
    except:
        raise APIException(api_errors.ERROR_GENERAL_BAD_PARA_FORMAT, 'Not valid integer format.')


def process_choices(value, choices):
    try:
        value = int(value)
    except ValueError:
        raise APIException(api_errors.ERROR_GENERAL_BAD_PARA_FORMAT)
    if value not in map(lambda x: x[0], choices):
        raise APIException(api_errors.ERROR_GENERAL_BAD_PARA_FORMAT)
    return value

def process_url(query_dict, process_fields=[]):
    try:
        for field in process_fields:
            if query_dict.get(field)!=None:
                query_dict[field] = query_dict.get(field)   #TODO: do url validation by regular expression
    except:
        raise APIException(api_errors.ERROR_GENERAL_BAD_PARA_FORMAT, 'Not valid url format.')

def wrap_info(response, info):
    return {'_response':response, '_info': info}


def get_now_ts(rtn_type='str'):
    ts = time.mktime(datetime.now().timetuple())
    if rtn_type == 'str':
        return str(ts).split('.')[0]
    else:
        return ts

def parse_pagination(offset=None, limit=None):
    try:
        offset = int(offset) if offset else 0
        limit = int(limit) if limit else DEFAULT_RETURN_NUM
        if limit > MAX_RETURN_NUM:
            limit = MAX_RETURN_NUM
    except ValueError:
        raise APIException(api_errors.ERROR_GENERAL_BAD_PARA_FORMAT, "The 'offset' and 'limit' must be integer.")
    return offset, limit


def process_request(cls, request, *args, **kwargs):
    user_in_session = request.session.get('user')

    if not request.user.is_authenticated():
        if request.method=='GET' and cls.read_auth_exempt:
            pass
        elif request.method=='POST' and cls.create_auth_exempt:
            pass
        elif user_in_session:
#            print "user_in_session: %s" % user_in_session
#            print "request.user: %s" % request.user
            if hasattr(request, 'user'):
                request.user = user_in_session
        else:
            raise APIException(api_errors.ERROR_AUTH_NOT_AUTHENTICATED)

    # Check authorized

    # For Backbone post data
    _post_json_dict = {}
    if "application/json" in request.META.get('CONTENT_TYPE', ''):
        _post_json_dict = simplejson.loads(request.raw_post_data)
    else:
        _post_json_dict = request.POST

    _resource_dict = cls.auth_resource(request=request, json_dict=_post_json_dict, **kwargs)
    if not _resource_dict:
        _resource_dict = {}
    _resource_dict['request_user'] = request.user

    # Validate Create Args
    if request.method == 'POST':
        _post = QueryDict('', mutable=True)
        # POST parameters
        _post['detail'] = request.POST.get('detail')=='true'

        # For Json
        content_type = request.META.get('CONTENT_TYPE', '')
        if "application/json" in content_type or content_type == '':
            if request.raw_post_data:
                json_dict = simplejson.loads(request.raw_post_data)
                for kwarg in cls.create_kwargs:
                    if json_dict.get(kwarg) == None and kwarg in cls.required_fields:
                        raise APIException(api_errors.ERROR_GENERAL_BAD_SIGNATURE, "'%s' is missing in params." % kwarg)
                    _post[kwarg] = json_dict.get(kwarg)
                _post['detail'] = json_dict.get('detail')==True

        # For XML
        else:
            for kwarg in cls.create_kwargs:
                if request.POST.get(kwarg) == None and kwarg in cls.required_fields:
                    raise APIException(api_errors.ERROR_GENERAL_BAD_SIGNATURE, "'%s' is missing in params." % kwarg)
                _post[kwarg] = request.POST.get(kwarg)
        # FILE parameters
        for kwarg in cls.files_kwargs:
            if request.FILES.get(kwarg) == None and request.POST.get('file64') == None and request.POST.get('url') == None:
                raise APIException(api_errors.ERROR_GENERAL_BAD_SIGNATURE, "'%s' is missing in upload file request." % kwarg)
            _post[kwarg] = request.FILES.get(kwarg)
        _post.update(_resource_dict)
        cls.create_validate(_post, request=request, **kwargs)
        request.CLEANED = _post
    # Pagination
    elif request.method == 'GET':
        _get = QueryDict('', mutable=True)
        _get['offset'], _get['limit'] = parse_pagination(request.GET.get('offset'), request.GET.get('limit'))
        _get['order_by'] = request.GET.get('order_by')
        _get['endpoint'] = _get['offset'] + _get['limit']
        _get['detail'] = request.GET.get('detail') == 'true'

        for required_field in cls.required_fields_for_read:
            if required_field not in request.GET:
                raise APIException(api_errors.ERROR_GENERAL_BAD_SIGNATURE, "'%s' is missing in params." % required_field)
            else:
                _get[required_field] = request.GET.get(required_field)

        for kwarg in cls.read_kwargs:
            if request.GET.get(kwarg) != None:
                _get[kwarg] = request.GET.get(kwarg)
        _get.update(_resource_dict)
        cls.read_validate(_get, request=request, **kwargs)
        request.CLEANED = cls.map_para(_get)
    # Validate Delete Args
    elif request.method == 'DELETE':
        _delete = QueryDict('', mutable=True)
        for kwarg in cls.delete_kwargs:
            _delete[kwarg] = request.GET.get(kwarg)
        _delete.update(_resource_dict)
        cls.delete_validate(_delete, request=request, **kwargs)
        request.CLEANED = _delete

    return request
