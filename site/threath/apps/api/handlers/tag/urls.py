from django.conf.urls.defaults import *

from api.resources import Resource

from handlers import IndexHandler

# from handlers import FriendHandler, SearchFriendHandler

urlpatterns = patterns('',
	url(r'^$', Resource(handler=IndexHandler)),
)
