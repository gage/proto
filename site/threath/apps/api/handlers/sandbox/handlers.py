import httplib2
import urllib2

from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.utils import simplejson
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

import api.errors as api_errors
from api.handlers.handlers import BaseHandler, BaseIndexHandler, BaseObjectHandler, BaseSearchHandler
from api.handlers.sandbox.threads import RebuildModelThread

from photos.models import Photo
from bson.objectid import ObjectId
from api.utils import create_sys_request
from api.handlers.photos.handlers import IndexHandler as PhotoIndexHandler


class SandboxHandler(BaseHandler):
    allowed_methods = ('GET', )

    def read(self, request):
        return 


class SandboxRebuildSolrHandler(BaseHandler):
    allowed_methods = ('GET', )

    def read(self, request):
        model = request.GET.get('model')
        RebuildModelThread(model).start()
        return 'success'


def template(request):
	handler = PhotoIndexHandler()
	sys_request = create_sys_request(request.user)
	rtn = handler.read(sys_request)
	return render_to_response('sandbox_template.html', {
    	'photo_collection': simplejson.dumps(rtn, cls=DateTimeAwareJSONEncoder, ensure_ascii=False)
    	}, context_instance = RequestContext(request))

def render_remote(request):
    url = request.GET.get('url')
    # url = urllib2.unquote(url)
    print url
    import httplib2
    h = httplib2.Http(".cache")
    resp, content = h.request(url, "GET")
    return HttpResponse(content)
    

def close_window(request):
    return render_to_response('api_close_window.html', context_instance = RequestContext(request))

