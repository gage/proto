from django.conf.urls.defaults import *
from api.resources import Resource
from handlers import PlaceFoursquareHandler, PlaceFoursquareObjectHandler, PlaceFoursquarePhotoHandler, PlaceFoursquareSearchHandler

urlpatterns = patterns('',
	url(r'^fs/explore/?$', Resource(handler=PlaceFoursquareHandler)),
    url(r'^fs/search/?$', Resource(handler=PlaceFoursquareSearchHandler)),
    url(r'^fs/(?P<object_id>\w+)/?$', Resource(handler=PlaceFoursquareObjectHandler)),
    url(r'^fs/(?P<fs_id>\w+)/photos/?$', Resource(handler=PlaceFoursquarePhotoHandler)),
)