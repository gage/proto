from django.conf.urls.defaults import *

from api.resources import Resource

from handlers import MeHandler, SearchHandler
from handlers import ObjectHandler, IndexHandler

# from handlers import FriendHandler, SearchFriendHandler

urlpatterns = patterns('',
	url(r'^$', Resource(handler=IndexHandler)),
    url(r'^me/?$', Resource(handler=MeHandler)),
    url(r'^me/\w+/?$', Resource(handler=MeHandler)),
    url(r'^search/?$', Resource(handler=SearchHandler)),

    url(r'^(?P<object_id>\w+)/?$', Resource(handler=ObjectHandler)),
    # url(r'^(?P<object_id>\w+)/friends/?$', Resource(handler=FriendHandler)),
)
