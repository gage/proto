__author__ = ""

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from api.handlers.handlers import BaseIndexHandler, BaseObjectHandler, BaseHandler, BaseSearchHandler
from api.errors import APIException
from api.utils import process_boolean, wrap_info
import api.errors as api_errors

from django.conf import settings


class IndexHandler(BaseIndexHandler):
    allowed_methods = ('GET', )

    def read(self, request):
        return ['123', 'hello', 'gg']

