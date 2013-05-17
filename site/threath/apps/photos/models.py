""" Photo models """

import datetime
import logging
import urllib
import uuid, os, re
import hashlib

from django.core.files import File
from django.core.files.storage import DefaultStorage
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.auth.models import User
from djangotoolbox.fields import ListField, SetField
from django.db.models.signals import post_save, post_delete, pre_delete
from django.db.models import F
from django.utils.encoding import smart_str

from globals.utils import get_django_ct, get_logger
from globals.contrib import MongoDBManager
from imagekit.lib import Image
from photos.imagespecs import *


def imagespecfilter(x, baseclass):
    return issubclass(x.__class__, baseclass)


def get_photo_upload_path(instance, filename):
    name_hash = hashlib.md5(filename).hexdigest()
    return os.path.join('photos',name_hash[0:2], name_hash[2:4], name_hash[4:6], name_hash[6:8], filename)


class BasePhoto(models.Model):
    """ Abstract photo base class """
    user            = models.ForeignKey(User, related_name="user_uploaded_photos")

    # Generic association
    content_type    = models.ForeignKey(ContentType, null=True, blank=True)
    object_id       = models.TextField(null=True, blank=True)
    content_object  = GenericForeignKey()

    image           = models.ImageField(upload_to=get_photo_upload_path)
    title           = models.CharField(max_length=255, null=True, blank=True)
    description     = models.TextField(null=True, blank=True)

    user_default    = models.BooleanField(default=False)
    album_default   = models.BooleanField(default=False)
    all_default     = models.BooleanField(default=False)
    group_default    = models.BooleanField(default=False)
    # !!!!!!!!!!!!!!!!!!!! When you add a default field, please add it into "is_default()" to avoid photo deletion during test

    created         = models.DateTimeField(default=datetime.datetime.now)

    ensure_cache    = models.BooleanField(default=False)

    width           = models.FloatField(default=0)
    height          = models.FloatField(default=0)
    filesize        = models.IntegerField(default=0)
    
    # old specs
    image32x32      = Image32x32()
    image50x50      = Image50x50()
    sepia50x50      = Sepia50x50()
    image105x105    = Image105x105()
    image150x150    = Image150x150()
    image480xany    = Image480xAny()

    # specs
    i32             = Image32x32()
    i64             = Image64x64()
    i128            = Image128x128()
    i256            = Image256x256()
    i512            = Image512x512()
    i60x105         = Image60x105()
    i120x177        = Image120x177()

    i98             = Image98x98()
    original        = ImageJpeg()

    img_list = [k for (k, v) in locals().items() if imagespecfilter(v, ImageSpecField)]

    def __unicode__(self):
        return "%s %s" % (self.pk, self.title)

    class Meta:
        abstract = True
        get_latest_by = 'created'
        verbose_name = _("photo")
        verbose_name_plural = _("photos")

    def is_default(self):
        return self.user_default or self.album_default or self.all_default or self.group_default

    def target_id(self):
        return self.object_id

    def attach(self, obj):
        """ Attaches this photo to obj, updates content_type and object_id """

        self.content_type = ContentType.objects.get_for_model(obj)
        self.object_id = obj.id
        self.save()

    def get_photo_url(self):
        try:
            return self.ImageJpeg.url
        except:
            return None

    def get_absolute_url(self):
        return self.get_photo_url()

    def get_model_type_name(self):
        return _('Photo')

    def get_title(self):
        if not self.title:
            self.title = os.path.basename(self.image.name).split('.')[0]
            self.__class__.objects.filter(id=self.id).update(title=self.title)

        return self.title

    def get_filesize(self):
        # Lazy build filesize
        if self.filesize == 0:
            self.filesize = self.image.size
            self.__class__.objects.filter(id=self.id).update(filesize=self.filesize)

        return self.filesize

class PhotoManager(MongoDBManager):
    pass

""" Non-abstract version of the BasePhoto class """
class Photo(BasePhoto):
    
    SOURCE_OTHER = 0
    SOURCE_LIBRARY = 1
    SOURCE_PHOTO_STREAM = 2
    SOURCE_FACEBOOK = 3
    SOURCE_INSTAGRAM = 4

    SOURCE_CHOICES = (
        (SOURCE_OTHER, 'Other'),
        (SOURCE_LIBRARY, 'Library'),
        (SOURCE_PHOTO_STREAM, 'Photo stream'),
        (SOURCE_FACEBOOK, 'Facebook'),
        (SOURCE_INSTAGRAM, 'Instagram'),
    )
    source = models.IntegerField(choices=SOURCE_CHOICES, default=SOURCE_OTHER)

    objects = PhotoManager()

    def save(self, *args, **kwargs):
        """ Sets user to AnonymousUser if not already set. """
        if not self.user_id:
            try:
                self.user = User.objects.get(username="AnonymousUser")
            except User.DoesNotExist:
                self.user = User.objects.create_user("AnonymousUser", "anonymoususer@example.com", "4a9Dadf123ad8A")

        if self.image:
            self.width = self.image.width
            self.height = self.image.height
            self.get_title()
            self.get_filesize()
            self._ensure_cache()

        super(BasePhoto, self).save(*args, **kwargs)

    def _get_action_name(self):
        return ''

    def _get_notify_name(self):
        return ''

    def picture(self):
        return self.to_json()

    def photo_source(self):
        return dict(self.SOURCE_CHOICES)[self.source]


    def _ensure_cache(self, force=False):
        if self.ensure_cache and not force:
            return

        for key in self.img_list:
            obj = getattr(self, key)
            if not os.path.exists(obj.path):
                obj.generate()
                
        self.ensure_cache = True
        self.ensure_fit = True
        self.__class__.objects.filter(id=self.id).update(ensure_cache=True)

    def to_json(self, detail=False, fields=None, **kwargs):
        request = kwargs.get('request', None)

        prefix, dot, sub = self.original.url.rpartition('original.')
        extension_match = re.match(r'.*(\.[^\.]*)$',self.original.url)
        try:
            extension = extension_match.group(1)
        except:
            extension = '.jpe'
        sizes = ['i32', 'i64', 'i128', 'i256', 'i512', 'i60x105', 'i120x177', 'original']
        urls = []
        for s in sizes:
            urls.append(getattr(self, s).url)

        rtn = {
            'id': self.pk,
            'prefix': '%s' % prefix,
            'extension': extension,
            'sizes': sizes,
            'filesize': self.filesize,
            'title': self.title,
            'original_raw': self.image.url,
            'original_width': self.width,
            'original_height': self.height,
        }
        if detail:
            object_id = self.object_id if self.object_id else self.id
            content_type = get_django_ct(self.content_type) if self.content_type else 'photos.photo'
            extended = {
                'original_raw': self.image.url,
                'original': self.original.url,
                'original_width': self.width,
                'original_height': self.height,
                'user_id': self.user.id,
                'user_display_name': self.user.get_profile().get_display_name(),
                'created': self.created,
                'object_id': object_id,
                'content_type': content_type,
            }
            rtn.update(extended)

        image_size = None
        if request:
            image_size = request.CLEANED.get('image_size', None)
        if kwargs.get('image_size'):
            image_size = kwargs['image_size']

        if image_size:
            extended = {
                'custom': getattr(self, image_size).url,
            }
            rtn.update(extended)

        # Extend rtn by extend attr
        if kwargs.get('extend'):
            rtn.update(kwargs['extend'])

        if fields:
            for each_field in rtn.keys():
                if each_field not in fields:
                    rtn.pop(each_field)

        return rtn

    def delete(self, *args, **kwargs):
        logger = get_logger('photo_delete', level=logging.DEBUG)
        # Don't delete default photos
        if self.is_default():
            return

        for spec_file in self._ik.spec_files:
            spec_file.clear()
        # remove image file
        if Photo.objects.filter(image=self.image.name).count()<=1:
            try:
                os.remove(self.image.path)
            except OSError as err:
                print err

        super(Photo, self).delete(*args, **kwargs)

class InvalidImageException(Exception):
    pass


def get_picture_from_url(img_url, alter_name=None, update_photo=None, get_raw_file=False):
    """
    By default, we use uuid_as_name because this can promise that in multiple threads situation
    no filename will be the same with each other.
    """
    if img_url:
        try:
            path = settings.DOWNLOAD_DIRECTORY + str(uuid.uuid4())
            filename = uuid.uuid4()

            content = urllib.urlretrieve(smart_str(img_url),path)
            content_type = content[1]['content-type']
            
            if 'image' in content_type:
                filetype = '.' + content_type.split('/')[1]
            else:
                raise InvalidImageException

            # Verify picture
            image = Image.open(content[0])
            image.verify()

            if get_raw_file:
                return open(content[0])

            target_file = File(open(content[0]))
            name = '%s%s'%(filename, filetype)
            photo = update_photo if update_photo else Photo()
            photo.image.save(name, target_file, save=True)
            os.remove(content[0])
            return photo
        except Exception, e:
            import traceback, sys
            etype, value, tb = sys.exc_info()
            print('%s\n' % ''.join(traceback.format_exception(etype, value, tb, 20)))
            return None
    else:
        return None

def on_delete_user(sender, **kwargs):
    print 'pre delete user in photos'
    user = kwargs['instance']
    photo_ids = Photo.objects.filter(user=user).values_list('id', flat=True)
    ps = Photo.objects.filter(user=user)
    for p in ps:
        p.delete()


pre_delete.connect(on_delete_user, sender=User)


