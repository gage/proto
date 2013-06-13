from django.conf.urls.defaults import *
from api.resources import Resource
from handlers import PlaceFoursquareHandler, PlaceFoursquareObjectHandler

urlpatterns = patterns('',
    url(r'^fs/search/?$', Resource(handler=PlaceFoursquareHandler)),
    url(r'^fs/(?P<object_id>\w+)/?$', Resource(handler=PlaceFoursquareObjectHandler)),
)