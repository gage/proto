""" User profile models """

import uuid
import hashlib
import smtplib
import time
import datetime
from random import shuffle

from django.db import models
from django.core.files import File
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlencode
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.conf import settings

from djangotoolbox.fields import ListField, DictField, SetField, EmbeddedModelField
from imagekit.lib import Image
from bson.objectid import ObjectId

from globals.contrib import MongoDBManager
from globals.timezones import TIMEZONE_CHOICES
from facebook.models import FacebookProfile
from photos.models import Photo
from slug.models import Slug


class Setting(models.Model):
    notify_sound = models.BooleanField(default=True)
    notify_vibration = models.BooleanField(default=True)
    message_prview = models.BooleanField(default=True)

    def set_field(self, user_profile, field, field_value):
        if field not in ('notify_sound', 'notify_vibration', 'message_prview'):
            raise LookupError

        if field_value not in (True, False):
            raise TypeError

        profile_id = user_profile.id
        UserProfile.objects.set('setting.'+field, profile_id, field_value)
        setattr(self, field, field_value)

    def to_json(self):
        rtn = {
            'notify_sound': self.notify_sound,
            'notify_vibration': self.notify_vibration,
            'message_prview': self.message_prview
        }
        return rtn

    def __unicode__(self):
        display_list = []
        for field in self._meta.fields:
            if field.name is 'id':
                continue
            display_list.append(field.name+': %s' % self.__dict__[field.name])
        return ', '.join(display_list)


class UserProfileManager(MongoDBManager):

    def get_default_photo(self):
        try:
            return Photo.objects.filter(user_default=True)[0]
        except IndexError:
            user_fallback = '%s/photos/%s' % (settings.MEDIA_ROOT, 'img_user_fallback.png')
            try:
                fp = open(user_fallback,'r')
                image = Image.open(fp)
                image.verify()
                photo = Photo(user_default=True)
                photo.save()
                Photo.objects.filter(pk=photo.pk).update(image='photos/img_user_fallback.png')
                photo = Photo.objects.get(pk=photo.pk)
                fp.close()
                return photo
            except:
                user_fallback = '%s/images/%s' % (settings.GLOBALS_STATIC_ROOT, 'img_user_fallback.png')
                fp = open(user_fallback,'r')
                image = Image.open(fp)
                image.verify()
                fp2 = open(user_fallback,'r')
                target_file = File(fp2)
                name = 'img_user_fallback.png'
                photo = Photo(user_default=True)
                photo.image.save(name, target_file, save=True)
                fp.close()
                fp2.close()
                return photo

    def check_if_email_has_been_used(self, email, exclude_inactive=False, exclude_user=None):
        email = email.lower()

        params = {
            'email__iexact': email,
        }
        query_dict = {
            'other_emails.email_address': email,
        }
        if exclude_inactive:
            params['is_active'] = True
            query_dict['is_active'] = True

        if not exclude_user:
            if User.objects.filter(**params).exists():
                return True
        else:
            if User.objects.filter(**params).exclude(id=exclude_user.id).exists():
                return True

            query_dict['user_id'] = {'$ne': ObjectId(exclude_user.id)}

        #Check secondary emails
        user_profiles = UserProfile.objects.raw_query(query_dict)
        if user_profiles:
            return True

        return False

    def get_anonymous(self):
        anonymous = User.objects.get(username='AnonymousUser')
        return anonymous


class UserProfile(models.Model):
    """ User profile model
    """
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.ForeignKey(User, related_name="userprofile")

    birthday = models.DateField(null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True, choices=GENDER_CHOICES)

    main_profile_pic = models.ForeignKey(Photo, null=True, blank=True, related_name='user_main_profile_pic')

    system_gen_password = models.CharField(max_length=20, null=True, blank=True)
    has_password = models.BooleanField(default=False)

    full_name = models.CharField(max_length=60, null=True, blank=True)

    # Collection: Basics
    user_agent = models.TextField(null=True, blank=True) # from HTTP header
    accept_language = models.TextField(null=True, blank=True) # from HTTP header

    # Notification
    setting = EmbeddedModelField('Setting', null=True) 
    username = models.CharField(max_length=40)

    #slug
    slug = models.ForeignKey(Slug, null=True, related_name='user-slug')

    objects = UserProfileManager()

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        user = self.user
        if user:
            user.name = self.get_display_name()
            user.image = self.main_profile_pic.image
            user.save()

    def __getattribute__(self, key):
        if key == 'username':
            if not object.__getattribute__(self, 'username') and self.id:
                self.username = self.user.username
                self.save()
                return self.username

        if key == 'main_profile_pic':
            if not object.__getattribute__(self, 'main_profile_pic'):
                try:
                    default_photo = Photo.objects.filter(user_default=True)[0]
                    return default_photo
                except IndexError:
                    user_fallback = '%s/photos/%s' % (settings.MEDIA_ROOT, 'img_user_fallback.png')
                    try:
                        fp = open(user_fallback,'r')
                        image = Image.open(fp)
                        image.verify()
                        photo = Photo(user_default=True)
                        photo.save()
                        Photo.objects.filter(pk=photo.pk).update(image='photos/img_user_fallback.png')
                        photo = Photo.objects.get(pk=photo.pk)
                        fp.close()
                        return photo
                    except Exception, e:
                        user_fallback = '%s/images/%s' % (settings.GLOBALS_STATIC_ROOT, 'img_user_fallback.png')
                        fp = open(user_fallback,'r')
                        image = Image.open(fp)
                        image.verify()
                        fp2 = open(user_fallback,'r')
                        target_file = File(fp2)
                        name = 'img_user_fallback.png'
                        photo = Photo(user_default=True)
                        photo.image.save(name, target_file, save=True)
                        fp.close()
                        fp2.close()
                        return photo

        return object.__getattribute__(self, key)

    def get_default_photo(self):
        try:
            return Photo.objects.filter(user_default=True)[0]
        except IndexError:
            return self.get_display_photo()

    def get_display_name(self):
        if self.full_name:
            return self.full_name
        else:
            return "%s %s" % (self.user.first_name, self.user.last_name)

    def get_display_photo(self):
        return self.main_profile_pic

    def get_profile(self):
        return self

    def get_username(self):
        return self.user.username

    def email(self):
        return self.user.email

    def to_json(self, request=None, detail=False, simple=False, **kwargs):
        rtn = {
            'id': self.user.pk,
            'full_name': self.get_display_name(),
            'username': self.user.username,
            'email': self.user.email,
        }
        if not simple:
            extended = {
                'photo': self.get_display_photo().to_json(**kwargs)
            }
            rtn.update(extended)

        if detail and request.user == self.user:
            pass

        return rtn


def create_profile(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created'] == True:
        new_slug = Slug(slug = user.username, content_object=user)
        new_slug.save()
        up = UserProfile.objects.create(user=user, slug=new_slug)

post_save.connect(create_profile, sender=User)


def on_delete_user(sender, **kwargs):
    user = kwargs['instance']
    UserProfile.objects.filter(user=user).delete()

pre_delete.connect(on_delete_user, sender=User)

