import json
import Queue
import time
import api.errors as api_errors

from urllib2 import HTTPError

from django.core.cache import cache
from api.errors import APIException
from api.handlers.handlers import BaseHandler, BaseObjectHandler
from api.utils import process_latlon, process_boolean, process_integer
from soundcloud.models import SoundCloud
from soundcloud.utils import BillboardProcessor, SoundCloudProcessor, DEFAULT_BILLBOARD_TOP_SONG_NUM
from globals.utils import is_mongo_pk 


class SoundCloudTopHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read_validate(self, query_dict, **kwargs):
        pass

    def read(self, request):
        ts = SoundCloud.objects.get_latest_ts()
        if not ts:
            raise APIException(api_errors.ERROR_SOUNDCLOUD_NO_TOP_SOUNDS)

        rtn = SoundCloud.objects.filter(is_ranking=True, ranking_ts=ts).order_by('ranking')

        return [song.to_json(request=request) for song in rtn] 


class SoundCloudSearchHandler(BaseHandler):
    allowed_methods = ('GET',)
    read_kwargs = ('q',)

    def read_validate(self, query_dict, **kwargs):
        pass

    def read(self, request):
        q = request.CLEANED.get('q', '')
        sounds = SoundCloud.objects.search(q)

        return [song.to_json(request=request) for song in sounds] 


class SoundCloudBuilderHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read_validate(self, query_dict, request, **kwargs):
        if not request.user.is_superuser:
            raise BaseAPIException(api_errors.ERROR_AUTH_NOT_AUTHORIZED)
        process_boolean(query_dict, ('is_task',))

    def read(self, request):
        is_task = request.GET.get('is_task')
        rtn = SoundCloudProcessor.build_top_sounds(DEFAULT_BILLBOARD_TOP_SONG_NUM, is_task=is_task)
        if is_task:
            return 'Done'
        return [song.to_json(request=request) for song in rtn] 


class SoundCloudObjectHandler(BaseObjectHandler):
    query_model = SoundCloud
    allowed_methods = ('GET', 'POST')

    def read_validate(self, query_dict, object_id, **kwargs):
        if is_mongo_pk(object_id):
            query_dict['obj'] = SoundCloud.objects.get(id=object_id)
        else:
            obj = SoundCloud.objects.create_object_by_id(object_id)
            query_dict['obj'] = obj

    def read(self, request, object_id):
        obj = request.CLEANED['obj']
        fields = {k: request.CLEANED[k] for k in ('detail', )}
        return obj.to_json(request=request, **fields)

    create_validate = read_validate
    create = read 
