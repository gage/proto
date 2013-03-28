from django import template
from iptolocation.models import Country, IPRange
import pdb
import iptolocation.models 

register = template.Library()

def easy_tag(func):
    """deal with the repetitive parts of parsing template tags"""
    def inner(parser, token):
        try:
            return func(*token.split_contents())
        except TypeError:
            raise template.TemplateSyntaxError('Bad arguments for tag "%s"' % token.split_contents()[0])
    inner.__name__ = func.__name__
    inner.__doc__ = inner.__doc__
    return inner



class GetCountryNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
        
    def render(self, context):
        ip = context['request'].META['REMOTE_ADDR']
        try:
            real_ip = context['request'].META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            pass
        else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs. Take just the first one.
            ip = real_ip.split(",")[0]
        ip = '220.136.178.253'   #testing
        iplong = iptolocation.models.ip_to_long(ip)
        ret = IPRange.objects.filter(start__lte=iplong).filter(end__gte=iplong)[0]
        context[self.varname] = ret.country.name
        return ''

@register.tag
@easy_tag
def get_country(_tag, _as, varname):
    return GetCountryNode(varname)


