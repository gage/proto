from haystack.fields import SearchField, FacetCharField
from haystack import indexes

# Built for unstemmed search
class GeneralTextField(SearchField):
    field_type = 'text_general'

    def __init__(self, **kwargs):
        if kwargs.get('facet_class') is None:
            kwargs['facet_class'] = FacetCharField

        super(GeneralTextField, self).__init__(**kwargs)

    def prepare(self, obj):
        return self.convert(super(GeneralTextField, self).prepare(obj))

    def convert(self, value):
        if value is None:
            return None

        return unicode(value)


class MaxWordField(SearchField):
    field_type = 'textMaxWord'

    def __init__(self, **kwargs):
        if kwargs.get('facet_class') is None:
            kwargs['facet_class'] = FacetCharField

        super(MaxWordField, self).__init__(**kwargs)
        self.is_multivalued = True

    def prepare(self, obj):
        return self.convert(super(MaxWordField, self).prepare(obj))

    def convert(self, value):
        if value is None:
            return None

        return unicode(value)


class ExactField(SearchField):
    field_type = 'text_exact'

    def __init__(self, **kwargs):
        if kwargs.get('facet_class') is None:
            kwargs['facet_class'] = FacetCharField

        super(ExactField, self).__init__(**kwargs)
        self.type = 'text_exact'

    def prepare(self, obj):
        return self.convert(super(ExactField, self).prepare(obj))

    def convert(self, value):
        if value is None:
            return None

        return unicode(value)

