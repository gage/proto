from django.contrib.auth.models import User
from django.conf import settings
from hashlib import sha256
from django.db.models.signals import post_save
from django.db import models
from globals.contrib import MongoDBManager
from photos.models import Photo

def get_display_name(self):
    #print "in User model - get_display_name()"
    if not self.full_name:
        self.full_name = self.get_profile().get_display_name()
        self.save()
    elif self.full_name == self.username:
        self.full_name = self.get_profile().get_display_name()
        if self.full_name != self.username:
            self.save()

    if not self.full_name:
        return self.username
    else:
        return self.full_name

def get_image_url(self, spec="image32x32"):
    #print "in User model - get_image_url()"
    if not self.image:
        self.image = self.get_profile().main_profile_pic.image
        self.save()       
    
    photo = Photo(image=self.image)
    return getattr(photo, spec).url


def generate_msn_email_hash(self):
    if self.email and not self.msn_email_hash:
        msn_client_id = settings.MSN_CLIENT_ID
        raw_str = self.email + msn_client_id
        hash_str = sha256(raw_str.lower()).hexdigest()
        
        self.msn_email_hash = hash_str
        self.save()    

def to_json(self, simple=None, **kwargs):
    extra_query_fields= kwargs.get('extra_query_fields')
    image_spec = kwargs.get('image_spec')
    
    if simple:
        rtn = {
            'id': self.id,
            'nickname': self.get_display_name(),
        }
        
        if extra_query_fields:
            for field in extra_query_fields:
                if field == "image":
                    rtn[field] = self.get_image_url() if not image_spec else self.get_image_url(image_spec)
                    print "image:%s" % rtn[field]
                else:
                    rtn[field] = getattr(self, field)() if callable(field) else getattr(self, field)
        
        return rtn
    else:
        return self.get_profile().to_json(**kwargs)

def is_user(self):
    return True

def is_first_login(self):
    return self.get_profile().is_first_login

def is_first_login_mobile(self):
    return self.get_profile().is_first_login_mobile

def _get_notify_name(self):
    return self.get_display_name()

User.add_to_class('_get_notify_name', _get_notify_name)
User.add_to_class("image", models.ImageField(upload_to='photos', null=True, blank=True))
User.add_to_class("full_name", models.CharField(max_length=50))
User.add_to_class("username_changed_count", models.IntegerField(default=0, null=True, blank=True))
User.add_to_class("msn_email_hash", models.CharField(max_length=80, null=True, blank=True))
User.add_to_class("is_guest", models.BooleanField(default=False))
User.add_to_class("get_display_name", get_display_name)
User.add_to_class("generate_msn_email_hash", generate_msn_email_hash)
User.add_to_class("get_image_url", get_image_url)
User.add_to_class('is_user', is_user)
User.add_to_class('to_json', to_json)
User.add_to_class('is_first_login', is_first_login)
User.add_to_class('is_first_login_mobile', is_first_login_mobile)
User.add_to_class('mongo_objects', MongoDBManager())

