from django.conf.urls.defaults import *

from api.resources import Resource

from handlers import IndexHandler, ObjectHandler
from handlers import ShareToGroupHandler, CopyToMyAlbumHandler#, EmoticonHandler

urlpatterns = patterns('',
    url(r'^$', Resource(handler=IndexHandler)),
    
    url(r'^share_to_group/?$', Resource(handler=ShareToGroupHandler)),
    url(r'^copy_to_my_album/?$', Resource(handler=CopyToMyAlbumHandler)),
    
    url(r'^(?P<object_id>\w+)/$', Resource(handler=ObjectHandler)),
    # url(r'^(?P<object_id>\w+)/emoticon/$', Resource(handler=EmoticonHandler))
)
