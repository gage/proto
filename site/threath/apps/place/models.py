import datetime
from django.conf import settings
from django.db import models
from urlparse import urljoin
from djangotoolbox.fields import EmbeddedModelField, ListField, DictField
from photos.models import get_picture_from_url

from globals.contrib import MongoDBManager

class BasePlace(models.Model):
    name = models.CharField(max_length=100)
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    address = models.CharField(max_length=255)
    short_address = models.CharField(max_length=255)    # Address excluding state code, country code, country name and postal code
    phone = models.CharField(max_length=25, default='', null=True, blank=True)
    display_phone = models.CharField(max_length=25, default='', null=True, blank=True)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def to_json(self, request=None, detail=False, **kwargs):
        rtn = {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lon': self.lon,
            'address': self.address,
            'phone': self.phone,
            'display_phone': self.display_phone,
        }
        return rtn

class FoursquarePlaceManager(MongoDBManager):
    def spatial_search(self, ll, q='', radius=100000, limit=20, section=None):
        from place.utils import FoursquarePlaceProcessor

        venues = FoursquarePlaceProcessor.spatial_search(ll=ll, q=q, radius=radius, limit=limit, section=section)
        return venues

class FoursquarePlace(BasePlace):

    ICON_SIZES = {
        'ss': 32,
        's': 44,
        'm': 64,
        'l': 88,
        'xl': 256
    }

    fid = models.CharField(max_length=30)
    # raw = models.TextField()

    category_id = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length=100, default='none')
    category_plural_name = models.CharField(max_length=100, default='none')
    category_short_name = models.CharField(max_length=100, default='none')
    icon_suffix = models.CharField(max_length=10, default='.png')
    icon_prefix = models.TextField(default='https://foursquare.com/img/categories/none_')

    # Location
    # Country Code
    cc = models.CharField(max_length=10, default='')
    city = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=50, default='')
    photo = models.ForeignKey('photos.Photo', null=True, blank=True)


    # Info
    checkins_count = models.IntegerField(default=0)
    tip_count = models.IntegerField(default=0)
    users_count = models.IntegerField(default=0)
    _distance = models.FloatField(default=0)
    rating = models.FloatField(default=-1)

    # Tips
    tips = ListField(null=True, blank=True)
    specials = ListField(null=True, blank=True)
    fs_photo = DictField(null=True, blank=True)

    # Photo processed
    _pp = models.BooleanField(default=False)

    # Section
    _section = models.CharField(max_length=50, null=True, blank=True)

    created = models.DateTimeField(default=datetime.datetime.now)

    objects = FoursquarePlaceManager()

    def __unicode__(self):
        return '%s %s%s%s (%s,%s)' % (self.name, self.country, self.city, self.address, self.lat, self.lon)

    def get_catetory_icon(self, size='s'):
        if self.icon_prefix == '':
            return "%s%s%s" % ('https://foursquare.com/img/categories/none_', self.ICON_SIZES[size], '.png')
        return "%s%s%s" % (self.icon_prefix, self.ICON_SIZES[size], self.icon_suffix)

    def is_restaurant(self):
        return self.icon_prefix and 'food' in self.icon_prefix

    @property
    def title(self):
        return self.name

    @property
    def section(self):
        if self._section==None:
            self._section = self._gen_section()
            if self.id:
                self.__class__.objects.filter(id=self.id).update(_section=self._section)
            return self.section
        else:
            return self._section

    @property
    def has_processed_photo(self):
        return self._pp

    def get_photo(self):
        if self.photo:
            return self.photo.to_json()
        else:
            from photos.models import Photo
            # Has not processed photo -> fetch it from foursquare
            if not self.has_processed_photo:
                fs_photo = self.fs_photo
                if not fs_photo:
                    pass
                else:
                    image_url = fs_photo['prefix'] + 'original' + fs_photo['suffix']
                    self.photo = get_picture_from_url(image_url)
                    if self.photo:
                        self._pp = True
                        self.__class__.objects.filter(id=self.id).update(photo=self.photo.id, _pp=True)
                        return self.photo.to_json()

            photo = Photo.objects.filter(restaurant_default=True)
            if photo:
                return photo[0].to_json()
            else:
                return {}

    def picture(self):
        return self.get_photo()

    def _gen_section(self):
        if self.icon_prefix == '':
            return 'none'
        elif 'categories_v2' in self.icon_prefix:
            strings = self.icon_prefix.split('categories_v2/')
            return strings[-1].split('/')[0]
        elif 'categories' in self.icon_prefix:
            strings = self.icon_prefix.split('categories/')
            return strings[-1].split('/')[0]

    def to_json(self, request=None, detail=False, **kwargs):
        rtn = super(FoursquarePlace, self).to_json(request=None, detail=False, **kwargs)
        rtn.update({
            'fid': self.fid,
            'category': self.category,
            'section': self.section,
            'fs_photo': self.fs_photo,
            'distance': self._distance,
        })
        if detail:
            rtn.update({
                'tips': self.tips,
                'photo': self.get_photo(),
                'checkins': self.checkins_count,
                'rating': self.rating,
                'cc': self.cc,
                'city': self.city,
                'state': self.state,
                'category_plural_name': self.category_plural_name,
                'category_short_name': self.category_short_name,
                'CLIENT_ID': settings.FOURSQUARE_CONSUMER_KEY
            })

        return rtn
