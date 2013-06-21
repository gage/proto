from django.conf.urls.defaults import *
from api.resources import Resource
from handlers import SoundCloudObjectHandler, SoundCloudTopHandler, SoundCloudBuilderHandler, SoundCloudSearchHandler

urlpatterns = patterns('',
    url(r'^search/?$', Resource(handler=SoundCloudSearchHandler)),
    url(r'^top/?$', Resource(handler=SoundCloudTopHandler)),
    url(r'^top/build/?$', Resource(handler=SoundCloudBuilderHandler)),
    url(r'^(?P<object_id>\w+)/?$', Resource(handler=SoundCloudObjectHandler)),
)