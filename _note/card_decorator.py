from django.db.models import base
from django.contrib.contenttypes.models import ContentType
from card.models import Card


class handle_card_on_demand(object):
    """
    This decorator is used for wrapping the to_json() of the model which can generate a card by its instance and card spec.
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        def wrapped_f(**kwargs):
            #print "**kwargs: %s" % kwargs
            to_card = kwargs.get('to_card')
            create_card = kwargs.get('create_card')

            if hasattr(instance, 'card_type'):
                card_type = instance.card_type
                card = None
                if create_card:
                    card, created = Card.objects.get_or_create_a_card(instance, card_type)
                if to_card:
                    if card:
                        return card.card_dict
                    else:
                        return Card.objects.gen_a_card_dict(instance, card_type)
                else:
                    return self.func(instance, **kwargs)
            else:
                raise Exception("Can't find a card_type property in the object: %s" % instance)

        return wrapped_f


def ct_id(self):
    if not hasattr(self, '_ct_id'):
        self.__class__._ct_id = ContentType.objects.get_for_model(self).pk
    return self._ct_id


def card_content_meta_decorator(card_type):
    class CardContentMeta(base.ModelBase):
        def __new__(self, classname, bases, classdict):
            """
            add card_type as class attributes
            """
            classdict['card_type'] = card_type

            """
            decorate to_json() method
            """
            to_json_meth = classdict.get('to_json')

            if to_json_meth and callable(to_json_meth):
                classdict['to_json'] = handle_card_on_demand(to_json_meth)

            """
            add ct_id as a property method
            """
            classdict['ct_id'] = property(ct_id)


            newClass = super(CardContentMeta, self).__new__(self, classname, bases, classdict)

            return newClass
    return CardContentMeta

def on_delete_content_object(sender, **kwargs):
    instance = kwargs['instance']
    Card.objects.filter(object_id=instance.pk).delete()
    