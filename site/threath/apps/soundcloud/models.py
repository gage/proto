import datetime
import diff_match_patch as dmp_module

from django.conf import settings
from django.db import models
from urlparse import urljoin
from djangotoolbox.fields import EmbeddedModelField, ListField, DictField
from photos.models import get_picture_from_url

from globals.contrib import MongoDBManager


class SoundCloudManager(MongoDBManager):
    def create_object_by_id(self, sc_id):
        """
        If we have this object in socialite -> query from db and return
        else -> fetch from SoundCloud
        """
        from utils import SoundCloudProcessor
        try:
            obj = self.get(sid=sc_id)
            return obj
        except SoundCloud.DoesNotExist:
            pass

        sc_obj = SoundCloudProcessor.fetch(sc_id)
        if sc_obj:
            sc_obj.save()
            return sc_obj

        print sc_id
        # Errors
        return None

    def get_latest_ts(self):
        if self.filter(ranking_ts__isnull=False).exists():
            newest_song = self.filter(ranking_ts__isnull=False).order_by('-ranking_ts')[0]
            return newest_song.ranking_ts
        else:
            return None

    def search(self, q):
        from utils import SoundCloudProcessor
        sounds = SoundCloudProcessor.search(q)
        return sounds

    def get_best_match(self, song_name, singer):
        query = "%s, %s" % (song_name, singer)
        query = query.lower().replace('featuring', '').replace('&amp;', '')
        sounds = self.search(query)
        
        sounds = sorted(sounds, reverse=True, key=lambda x: x.playback_count)
        rtn = None
        for sound in sounds:
            # print sound

            # print sound, sound.user['username'], sound.playback_count
            dmp = dmp_module.diff_match_patch()
            
            dmp.Match_Threshold = 0.1
            if sound.track_type == 'remix':
                continue

            if dmp.match_main(sound.title, 'remix', 0) != -1:
                continue

            dmp.Match_Threshold = 0.4    
            # print sound.playback_count, sound.title, song_name, dmp.match_main(sound.title, song_name, 0)
            if dmp.match_main(sound.title, song_name, 0) != -1:
                # if not rtn:
                #     print '!!!!!!!!!!!', sound.title, sound.user['username'], sound.playback_count
                rtn = sound if not rtn else rtn
            else:
                pass
                # print 'XXXX', sound.title, song_name
        # print rtn, song_name, singer
        return rtn


class SoundCloud(models.Model):

    sid = models.CharField(max_length=30)
    embeddable_by = models.CharField(max_length=30)
    # raw = models.TextField()

    photo = models.ForeignKey('photos.Photo', null=True, blank=True)

    # Info
    _raw = DictField()

    # Photo processed
    _pp = models.BooleanField(default=False)
    created = models.DateTimeField(default=datetime.datetime.now)
    ranking_ts = models.IntegerField(null=True)
    ranking = models.IntegerField(null=True)
    is_ranking = models.BooleanField(default=False)

    objects = SoundCloudManager()

    def __unicode__(self):
        return self.title

    def __getattribute__(self, key):
        # Code Review: we don't need put all the attributes into model's fields
        if key in object.__getattribute__(self, 'dict_attrs'):
            if key == 'stream_url':
                return object.__getattribute__(self, '_raw').get(key, '')+"?client_id="+settings.SOUNDCLOUD_CLIENT_ID
            return object.__getattribute__(self, '_raw').get(key, None)
        return object.__getattribute__(self, key)

    @property
    def dict_attrs(self):
         return ('title', 'user', 'streamable', 'duration', 'purchase_url', 
                'original_format', 'permalink_url', 'artwork_url', 'stream_url',
                'playback_count', 'comment_count', 'embeddable_by', 'track_type')

    @property
    def has_processed_photo(self):
        return self._pp

    @property
    def username(self):
        return self._raw['user']['username']

    def cover_url(self, size='300x300'):
        if self.artwork_url:
            return self.artwork_url.replace('large', 't'+size)
        else:
            # TODO: default
            return ''

    def get_photo(self):
        if self.photo:
            return self.photo.to_json()
        else:
            from photos.models import Photo
            # Has not processed photo -> fetch it from foursquare
            if not self.has_processed_photo:
                cover_url = self.cover_url(size='500x500')
                if not cover_url:
                    pass
                else:
                    self.photo = get_picture_from_url(cover_url)
                    if self.photo:
                        self._pp = True
                        self.__class__.objects.filter(id=self.id).update(photo=self.photo.id, _pp=True)
                        return self.photo.to_json()

            photo = Photo.objects.filter(all_default=True)
            if photo:
                return photo[0].to_json()
            else:
                return {}

    def picture(self):
        return self.get_photo()

    def image_img(self):
        if self.cover_url():
            return u'<a href="%s"><img src="%s" /></a>' % (self.cover_url(size='500x500'), self.cover_url(size='50x50'))
        else:
            return '(No Cover)'

    image_img.short_description = 'Thumb'
    image_img.allow_tags = True

    def to_json(self, request=None, detail=False, **kwargs):
        rtn = {
            'permalink_url': self.permalink_url,
            'title': self.title,
            'sid': self.sid,
            'cover': self.cover_url(size='500x500'),
            'thumb': self.cover_url(size='200x200'),
            'thumbnail': self.cover_url(size='80x80'),
            'duration': self.duration,
            'user': self.user,
            'stream_url': self.stream_url,
            'id': self.id if self.id else self.sid,
            'playback_count': self.playback_count
        }
        
        if detail:
            rtn.update({
            })

        return rtn
