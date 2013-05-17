import base64
import imghdr
import sys
import uuid
import re

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile

import api.errors as api_errors
from api.errors import APIException
from api.handlers.handlers import BaseHandler, BaseIndexHandler, BaseObjectHandler
from photos.models import Photo, get_picture_from_url
from photos.utils import base64_to_photo_obj
from api.utils import process_list, process_url


# ============== Index Handler =============
class IndexHandler(BaseIndexHandler):
    create_kwargs = ('title', 'description', 'file64', 'url', 'file')
    files_kwargs = ('file', )
    read_kwargs = ('id', 'target_id', 'user_id', 'place_id')
    allowed_filter = ('id', 'object_id', 'user', 'place')
    para_mapping = {
        'target_id':'object_id',
    }
    query_model = Photo
    read_auth_exempt = True

    def create_validate(self, query_dict, request, **kwargs):
        if query_dict['url']:
            process_url(query_dict, ['url', ])
            format = query_dict['url'].split('.')[-1]
        elif query_dict['file']:
            if query_dict['file'].size > settings.PHOTOS_MAX_SIZE:
                raise api_errors.APIException(api_errors.ERROR_PHOTOS_TOO_LARGE)
            format = imghdr.what('', h=query_dict['file'].read())
            if not query_dict['title']:
                try:
                    query_dict['title'] = query_dict['file'].name.split('.')[0]
                except:
                    query_dict['title'] = query_dict['file'].name
        elif query_dict['file64']:
            try:
                query_dict['photo'], format = base64_to_photo_obj(request.user, query_dict['file64'])
            except:
                raise APIException(api_errors.ERROR_PHOTOS_BASE64_DECODE_FAILED)
        else:
            raise api_errors.APIException(api_errors.ERROR_PHOTOS_NO_IMAGE)

        if format not in settings.PHOTOS_FORMATS:
            raise api_errors.APIException(api_errors.ERROR_PHOTOS_BAD_FORMAT)
        query_dict['format'] = format
            

    def create(self, request, raw=False, **kwargs):
        """ Uploads a new photo. """
        title = request.CLEANED.get('title', '')
        description = request.CLEANED.get('description', '')
        if request.CLEANED['url']:
            photo = get_picture_from_url(request.CLEANED['url'])
        elif request.CLEANED['file64']:
            photo = request.CLEANED['photo']
        else:
            if request.CLEANED['file']:
                uploaded_file = request.CLEANED['file']
            format = request.CLEANED['format']
            photo = Photo(user=request.user, title=title, description=description)
            photo.image.save("%s.%s" % (uuid.uuid4(), format), uploaded_file)
            photo.save()
            uploaded_file.close()

        return photo.to_json(request=request, detail=request.CLEANED['detail']) if not raw else photo
        

# ============== Object Handler =============
class ObjectHandler(BaseObjectHandler):
    query_model = Photo
    
# ============= Share(Copy) Photos to Specific Group's ==============
class ShareToGroupHandler(BaseHandler):
    allowed_methods = ('POST', )
    required_fields = ('group_id', 'photo_ids')
    
    def auth_resource(self, request, **kwargs):
        group_id = request.REQUEST.get('group_id')
        group = Group.objects.get(id=group_id)
        if not group.is_member(request.user):
            raise APIException(api_errors.ERROR_AUTH_NOT_AUTHORIZED)
            
        return {'group': group}
    
    def create_validate(self, query_dict, request, **kwargs):
        process_list(query_dict, ('photo_ids', ))
    
    def create(self, request):        
        photo_ids = request.CLEANED['photo_ids']
        group = request.CLEANED['group']
        photo_list = Photo.objects.batch_copy(photo_ids, group)
        return [photo.to_json(request=request, detail=request.CLEANED['detail']) for photo in photo_list]


# ============= Share(Copy) Photos to Myself ==============
class CopyToMyAlbumHandler(BaseHandler):
    allowed_methods = ('POST', )
    required_fields = ('photo_ids', )
    
    def create_validate(self, query_dict, request, **kwargs):
        process_list(query_dict, ('photo_ids', ))
    
    def create(self, request):
        photo_ids = request.CLEANED['photo_ids']
        photo_list = Photo.objects.batch_copy(photo_ids, request.user)
        return [photo.to_json(request=request, detail=request.CLEANED['detail']) for photo in photo_list]
        
