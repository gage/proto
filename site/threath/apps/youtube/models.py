import re
import urllib2
import chardet
import logging
from datetime import datetime, timedelta
from readability.readability import Document
from urlparse import urlparse

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django_mongodb_engine.contrib import MongoDBManager
from djangotoolbox.fields import SetField, ListField, EmbeddedModelField

from bson.objectid import ObjectId

from photos.models import Photo
import utils as youtube_utils

from globals.utils import fetch_image_from_url, get_logger
from globals.utils import http_url_re, strip_http_protocol

from optparse import OptionParser
from photos.models import get_picture_from_url


DEVELOPER_KEY = settings.GOOGLE_API_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class YoutubeVideoManager(MongoDBManager):
    def create_youtube_object_by_id(self, youtube_id):
        try:
            obj = self.get(youtube_id=youtube_id)
            return obj
        except YoutubeVideo.DoesNotExist:
            pass

        youtube_obj = youtube_utils.fetch(youtube_id)
        youtube_obj.pop('thumburl')
        obj, created = self.get_or_create(youtube_id=youtube_obj['youtube_id'], defaults=youtube_obj)
        return obj

    # Deprecated
    def youtube_search(self, options):
        # TODO: optimize this by caching the youtube service
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

        search_response = youtube.search().list(
            q=options.get('q', ''),
            part="id,snippet",
            maxResults=10
        ).execute()

        videos = self.__parse_youtube_result(search_response)
        print videos

        return [video.to_json() for video in videos]

    # Deprecated
    def __parse_youtube_result(self, raw):
        videos = []
        for search_result in raw.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                youtube_video_model_params = {
                    'youtube_id' : search_result["id"]["videoId"],
                    'title' : search_result["snippet"]["title"]
                }
                video = YoutubeVideo(**youtube_video_model_params)
                videos.append(video)

        return videos


class YoutubeVideo(models.Model):

    objects = YoutubeVideoManager()
    youtube_id = models.CharField(max_length=11)
    title = models.CharField(max_length=255)
    duration = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    photo = models.ForeignKey('photos.Photo', null=True, blank=True)
    # Photo processed
    _pp = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s" % (self.title, self.youtube_id)


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
                picture_url = self.picture_url
                if not picture_url:
                    pass
                else:
                    self.photo = get_picture_from_url(picture_url)
                    if self.photo:
                        self._pp = True
                        self.__class__.objects.filter(id=self.id).update(photo=self.photo.id, _pp=True)
                        return self.photo.to_json()

            photo = None
            if photo:
                return photo[0].to_json()
            else:
                return {}

    def picture(self):
        return self.get_photo()

    @property
    def picture_url(self):
        return self.get_thumbnail('hq')

    def get_thumbnail(self, size=''):
        '''
        size:
            '' => default
            'hq' ==> high quality
            'mq' ==> medium quality
        '''
        url = 'https://i.ytimg.com/vi/%s/%sdefault.jpg' % (self.youtube_id, size)

        return url

    def to_json(self, request=None, **kwargs):
        rtn = {
            'youtube_id': self.youtube_id,
            'title': self.title,
            'thumb': self.get_thumbnail(size='mq'),
            'view_count': self.view_count,
            'duration': self.duration
        }
        return rtn