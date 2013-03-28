import uuid
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
# from globals.jinja2 import JinjaTools

def global_common(request):

    return {
        'USE_LESS'  : settings.USE_LESS,
        'SITE_DOMAIN': settings.SITE_DOMAIN,
        'DEBUG': settings.DEBUG,
        # 'jinja': JinjaTools,
    }
