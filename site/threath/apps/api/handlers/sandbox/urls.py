from django.conf.urls.defaults import *

from api.resources import Resource

from handlers import SandboxHandler, SandboxRebuildSolrHandler

urlpatterns = patterns('',
    url(r'^$', Resource(handler=SandboxHandler)),
    url(r'^rebuild_solr/?$', Resource(handler=SandboxRebuildSolrHandler)),
    url(r'^close_window/$', 'api.handlers.sandbox.handlers.close_window', name="api-close-window"),
    url(r'^template/', 'api.handlers.sandbox.handlers.template', name="api-test-template"),
    url(r'^render_remote/$', 'api.handlers.sandbox.handlers.render_remote', name="api-test-render-remote"),
)
