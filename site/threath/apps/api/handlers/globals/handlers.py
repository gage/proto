from django.conf import settings

from api.handlers.handlers import BaseHandler
# from django.contrib.auth.models import User
# import api.errors as api_errors
# from api.errors import APIException


class WebviewHashHandler(BaseHandler):
    allowed_methods = ('GET',)
    read_auth_exempt = True

    def read(self, request):
        return {'hash': settings.DEVICE_WEBVIEW_MD5}
