import simplejson as json
import time

from django.db import models
from django.db.models.signals import pre_delete
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from globals.contrib import MongoDBManager
from djangotoolbox.fields import ListField, EmbeddedModelField
from card.specs import CARD_TYPE, CARD_TYPE_STRING, CARD_TYPE_CHOICE, CARD_SPEC

class CardEntityManager(MongoDBManager):
    pass


class CardEntity(models.Model):
    url = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_collection = models.BooleanField()
    json_str = models.TextField(null=True, blank=True)

    objects = CardEntityManager()

    class Meta:
        abstract = True


class CardManager(MongoDBManager):

    def gen_a_card_dict(self, content_object, card_type, card_id=None):
        card_dict = {}
        data = {}
        card_spec = CARD_SPEC[card_type]
        for field in card_spec:
            if hasattr(content_object, field):
                field_value = getattr(content_object, field)
                data[field] = field_value() if callable(field_value) else field_value
            else:
                data[field] = None

        card_dict['data'] = data
        card_dict['data']['ct_id'] = content_object.ct_id
        card_dict['card_type'] = card_type
        card_dict['card_type_str'] = CARD_TYPE_STRING[card_type]

        if card_id:
            card_dict['card_id'] = card_id
            
        return card_dict
            
    def gen_a_card_json_str(self, content_object, card_type, card_id=None):
        card_dict = self.gen_a_card_dict(content_object, card_type, card_id)
        
        card_json_str = json.dumps(card_dict, cls=DjangoJSONEncoder)
        return card_json_str

    def create_a_card(self, content_object, card_type):
        card = self.create(content_object=content_object, card_type=card_type)
        card.json_str = self.gen_a_card_json_str(content_object, card_type, card.pk)
        card.save()
        return card
    
    def get_or_create_a_card(self, content_object, card_type):
        if self.filter(object_id=content_object.pk, card_type=card_type).exists():
            card = self.get(object_id=content_object.pk, card_type=card_type)
            return card, False
        else:
            card = self.create_a_card(content_object, card_type)
            return card, True


class CardCollectionManager(MongoDBManager):
    pass


class Card(CardEntity):
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.CharField(max_length=255, null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    card_type = models.IntegerField(default=CARD_TYPE.UNDEFINED, choices=CARD_TYPE_CHOICE)

    objects = CardManager()

    @property
    def card_dict(self):
        return json.loads(self.json_str)

    def __unicode__(self):
        return "Card(card_type=%(card_type)s, card_type_str=%(card_type_str)s, object_id=%(object_id)s, content_type=%(content_type)s, json_str=%(json_str)s)" % \
                {
                 'card_type': self.card_type,
                 'card_type_str': CARD_TYPE_STRING[self.card_type],
                 'object_id': self.object_id,
                 'content_type': self.content_type,
                 'json_str': self.json_str
                 }

    def save(self, **kwargs):
        self.is_collection = False
        super(Card, self).save(**kwargs)

    def to_json(self, detail=False, attach_content_object=False, **kwargs):

        card_dict = self.card_dict
        data = card_dict.get('data')
        
        """
        This is used for renewing the card json when card spec has modified. 
        """
        spec_fields = CARD_SPEC[self.card_type]
        for field in spec_fields:
            if not field in data:
                try:
                    content_object = self.content_type.get_object_for_this_type(id=self.object_id)
                except ObjectDoesNotExist:
                    self.delete()
                    return {}
                else:
                    self.json_str = self.__class__.objects.gen_a_card_json_str(content_object, self.card_type, self.pk)
                    self.save()
                    card_dict = self.card_dict
                    data = card_dict.get('data')                    
                    break        

        """
        attach_content_object is used for Card Viewer
        """
        if attach_content_object:
            try:
                content_object = self.content_type.get_object_for_this_type(id=self.object_id)
            except ObjectDoesNotExist:
                self.delete()
                content_obj = {}
            else:
                content_obj = content_object.to_json(detail=True)            
            card_dict['content_object'] = content_obj
        
        if detail:
            return card_dict
        else:                        
            required_fields = ('id', 'title', 'picture')
            data = {k: data.get(k, "") for k in required_fields}
            
            if self.card_type == CARD_TYPE.LINK:
                url = card_dict.get('data').get('url')
                data.update({'url':url})            
            
            card_dict['data'] = data
            return card_dict
        
#        return {'card_id': self.id,
#                'is_collection': self.is_collection,
#                'json_str': self.json_str,
#                'card_type': self.card_type,
#                'card_type_str': CARD_TYPE_STRING[self.card_type],
#                }

class CardCollection(CardEntity):
    card_list = ListField(EmbeddedModelField(Card))

    objects = CardCollectionManager()

    def __unicode__(self):
        return "A Card Collection: %s" % self.card_list

    def save(self, **kwargs):
        self.is_collection = True
        self.json_str = json.dumps(self.card_list, cls=DjangoJSONEncoder)
        super(CardCollection, self).save(**kwargs)

    def to_json(self, detail=False, **kwargs):

        return {'id': self.id,
                'is_collection': self.is_collection,
                'json_str': self.json_str,
                }

class SharedCardManager(MongoDBManager):
    pass
        
class SharedCard(models.Model):
    group = models.ForeignKey('group.Group', null=True, blank=True)
    user = models.ForeignKey('auth.User', null=True, blank=True)
    card = models.ForeignKey(Card, null=True, blank=True)
    card_type = models.IntegerField(default=CARD_TYPE.UNDEFINED, choices=CARD_TYPE_CHOICE)
    created = models.DateTimeField(auto_now_add=True)
    
    objects = SharedCardManager()
    
    class Meta:
        ordering = ['-created']
    
    def __unicode__(self):
        return "Card(group=%(group_id)s, user=%(user_id)s, card=%(card_id)s)" % \
            {
             'group_id': self.group_id,
             'user_id': self.user_id,
             'card_id': self.card_id,
             }

    @property
    def _owner_id(self):
        return self.user_id if self.user_id else self.group_id
        
    def to_json(self, detail=False, **kwargs):
        
        try:
            self.card
        except ObjectDoesNotExist:
            self.delete()
            return {}
        
        rtn = {
#            'group_id': self.group_id,
#            'user_id': self.user_id,
            'id': self.id,
            'created': time.mktime(self.created.timetuple()),
            'card': self.card.to_json(detail, **kwargs)
        }
        
        return rtn

def on_delete_card(sender, **kwargs):
    card = kwargs['instance']
    SharedCard.objects.filter(card=card).delete()

pre_delete.connect(on_delete_card, sender=Card)

def on_delete_user(sender, **kwargs):
    user = kwargs['instance']
    for card in SharedCard.objects.filter(user=user):
        card.delete()

pre_delete.connect(on_delete_user, sender=User)

