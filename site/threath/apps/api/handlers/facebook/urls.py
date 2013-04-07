from django.conf.urls.defaults import *

from api.resources import Resource

from handlers import ConnectHandler

urlpatterns = patterns('',
    url(r'^connect/?$', Resource(handler=ConnectHandler)),
)
