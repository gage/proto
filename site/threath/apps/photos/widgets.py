""" Widgets for user profiles """

__author__ = "Hoang Xuan Phu <phu@cogini.com>"
__version__ = "1"

from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.encoding import force_unicode


class PhotoWidget(widgets.Input):

    input_type = 'hidden'

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        input_field = mark_safe(u'<input%s />' % flatatt(final_attrs))
        html = render_to_string('photo_widget.html', {'input_field': input_field})
        return mark_safe(html)

