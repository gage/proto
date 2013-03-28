from django.conf.urls.defaults import *

from api.resources import Resource

from handlers import WebviewHashHandler

urlpatterns = patterns('',
    # url(r'^$', Resource(handler=IndexHandler)),
    url(r'^webview_hash/?$', Resource(handler=WebviewHashHandler)),
)
