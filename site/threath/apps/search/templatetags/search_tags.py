""" Site search template tags """

__author__ = "Jason Ke <jason.ke@geniecapital.com.tw>"
__contributors__ = ["Jason Ke <jason.ke@geniecapital.com.tw>"]

from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def show_translated_city(context, city):
    request = context['request']
    city_name = None
    if city:
        city_name = city.get_display_name().split(',')[0]
    return city_name
