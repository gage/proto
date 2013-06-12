from django.contrib.auth.models import User
from django.core.cache import cache

import api.errors as api_errors
import re
from api.handlers.handlers import BaseHandler, BaseIndexHandler, BaseObjectHandler
from api.utils import get_target_object
from api.errors import APIException

from youtube.models import YoutubeVideo
from youtube.utils import youtube_search 
from gdata.service import RequestError
from django.contrib.contenttypes.models import ContentType
from globals.utils import is_mongo_pk 


class YoutubeIndexHandler(BaseIndexHandler):
    allowed_methods = ('GET', )
    read_kwargs = ('category', 'q', 'geo_code', 'time')
    
    def read_validate(self, query_dict, **kwargs):
        # TODO: verify geo_code
        options = {}
        for field in self.read_kwargs:
            if query_dict.get(field):
                options[field] = query_dict.get(field)
        query_dict['options'] = options
        time = options.get('time')
        if time and time not in ('today', 'this_week', 'this_month', 'all_time'):
            raise api_errors.APIException(api_errors.ERROR_YOUTUBE_QUERY_PARA_NOT_MATCH, '"time" should in today, this_week, this_month, or all_time.')

    def read(self, request):
        options = request.CLEANED['options']
        options['max_results'] = request.CLEANED['limit']
        options['start_index'] = request.CLEANED['offset']
        para_hash = hash(frozenset(options.items()))
        para_key = 'youtube_' + str(para_hash)
        if not cache.get(para_key):
            try:
                rtn = youtube_search(**options)
            except RequestError, e:
                raise api_errors.APIException(api_errors.ERROR_YOUTUBE_QUERY_PARA_NOT_MATCH, e)
            cache.set(para_key, rtn)
        else:
            rtn = cache.get(para_key)
        return rtn


class YoutubeObjectHandler(BaseObjectHandler):
    query_model = YoutubeVideo
    allowed_methods = ('GET', 'POST')
    read_auth_exempt = True

    def read_validate(self, query_dict, object_id, **kwargs):
        if is_mongo_pk(object_id):
            query_dict['obj'] = YoutubeVideo.objects.get(id=object_id)
        else:
            obj = YoutubeVideo.objects.create_youtube_object_by_id(object_id)
            query_dict['obj'] = obj

    def read(self, request, object_id):
        obj = request.CLEANED['obj']
        fields = {k: request.CLEANED[k] for k in ('detail', 'to_card', 'create_card')}
        return obj.to_json(request=request, **fields)

    create_validate = read_validate
    create = read 

