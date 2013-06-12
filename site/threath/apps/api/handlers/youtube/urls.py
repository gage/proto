from django.conf.urls.defaults import *

from api.resources import Resource

from handlers import YoutubeIndexHandler, YoutubeObjectHandler

urlpatterns = patterns('',
    url(r'^$', Resource(handler=YoutubeIndexHandler)),
    url(r'^(?P<object_id>\w+)/?$', Resource(handler=YoutubeObjectHandler)),
)
