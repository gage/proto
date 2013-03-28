from django.conf.urls.defaults import *

from api.resources import Resource

from handlers import LogoutHandler, GeneralSigninHandler

urlpatterns = patterns('',
    url(r'^logout/?$', Resource(handler=LogoutHandler)),

    url(r'^signin/?$', Resource(handler=GeneralSigninHandler)),
    url(r'^general_signin/?$', Resource(handler=GeneralSigninHandler)),
)
