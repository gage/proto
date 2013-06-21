import json
import time
from datetime import datetime
import urllib, urllib2
from BeautifulSoup import BeautifulSoup

from django.core.cache import cache
from django.utils.http import urlquote
from django.conf import settings
from django.utils.encoding import smart_str

from models import SoundCloud
from tasks import build_single_ranking_task

DEFAULT_BILLBOARD_TOP_SONG_NUM = 20

class SoundCloudProcessor(object):
    @classmethod
    def fetch(cls, sc_id):
        def _fetch(url):
            data = urllib2.urlopen(url).read()
            parsed_data = json.loads(data)
            sound = cls.__sc_process_obj(parsed_data)
            print sound
            return sound

        para_dict = {
            'client_id':settings.SOUNDCLOUD_CLIENT_ID
        }
        para = urllib.urlencode(para_dict)
        url = 'http://api.soundcloud.com/tracks/'+sc_id+'.json?'+para
        try:
            sounds = _fetch(url)
            return sounds
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
            try:
                sounds = _fetch(url)
                return sounds
            except urllib2.HTTPError, e:
                return None
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            return None


    @classmethod
    def build_top_sounds(cls, num=DEFAULT_BILLBOARD_TOP_SONG_NUM, is_task=False):
        songs = BillboardProcessor.top_hundred(num)
        if is_task:
            for idx in range(num):
                ranking = idx + 1
                build_single_ranking_task.delay(ranking, songs[idx])
        else:
            rtn = []

            for idx in range(num):
                ranking = idx + 1
                best_song = cls.build_single_ranking_song(ranking, songs[idx])
                rtn.append(best_song)

            return rtn

    @classmethod
    def build_single_ranking_song(cls, ranking, billboard_song):
        if billboard_song:
            song = billboard_song
        else:
            song = BillboardProcessor.top_hundred()[ranking-1]

        best_song = SoundCloud.objects.get_best_match(song['name'], song['singer'])
        if best_song:
            best_song.ranking_ts = time.mktime(song['pub_date'].timetuple())
            best_song.ranking = int(song['ranking'])
            best_song.is_ranking = True
            if SoundCloud.objects.filter(ranking_ts=best_song.ranking_ts, ranking=best_song.ranking, is_ranking=True).exists():
                best_song = SoundCloud.objects.filter(ranking_ts=best_song.ranking_ts, ranking=best_song.ranking, is_ranking=True)[0]
                # print best_song, 'exists'
            else:
                best_song.save()
                # print best_song, 'build'
            return best_song
        else:
            return None


    @classmethod
    def search(cls, q):
        def _fetch(url):
            data = urllib2.urlopen(url).read()
            sounds = cls.__sc_sound_parse(data)
            cache.set(url, sounds, 3600)
            return sounds

        para = {'client_id': settings.SOUNDCLOUD_CLIENT_ID, 'q': smart_str(q)}
        parameter = urllib.urlencode(para)
        url = 'http://api.soundcloud.com/tracks.json?%s' % parameter
        # print url

        if cache.get(url):
            return cache.get(url)
        try:
            sounds = _fetch(url)
            return sounds
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
            try:
                sounds = _fetch(url)
                return sounds
            except urllib2.HTTPError, e:
                return []
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            return []


    @classmethod
    def __sc_process_obj(cls, item):
        sc_sound_model = {'_raw': item}
        sc_sound_model['embeddable_by'] = item['embeddable_by']
        sc_sound_model['sid'] = item['id']
        sc_sound = SoundCloud(**sc_sound_model)
        return sc_sound

    @classmethod
    def __sc_sound_parse(cls, raw):
        json_data = json.loads(raw)
        sounds = []
        for item in json_data:
            if not item['streamable']:
                # skip if the sound is not streamable
                continue

            # Assign to its dict
            sc_sound = cls.__sc_process_obj(item)            
            sounds.append(sc_sound)

        sc_ids = [sound.sid for sound in sounds]
        sc_sounds_in_db = SoundCloud.objects.filter(sid__in=sc_ids).values_list('sid', 'id')
        sc_sounds_dicts = dict((x, y) for x, y in sc_sounds_in_db)
        for new_sound in sounds:
            if new_sound.sid not in sc_sounds_dicts.keys():
                pass
            else:
                new_sound.id = sc_sounds_dicts[new_sound.fid]

        return sounds


class BillboardProcessor(object):
    @classmethod
    def parse(cls, item):
        title_tag = item.title
        pub_date = None
        if item.pubdate:
            pub_date = datetime.strptime(item.pubdate.string, '%a, %d %b %Y %H:%M:%S GMT')

        ranking = title_tag.string.split(':')[0]
        title = title_tag.string.split(':')[1]
        song_name = title.split(',')[0]
        singer_name = title.split(',')[1]
        return  {
            'ranking': ranking,
            'name': song_name,
            'singer': singer_name,
            'pub_date': pub_date
        }

    @classmethod
    def top_hundred(cls, num=DEFAULT_BILLBOARD_TOP_SONG_NUM):
        key = 'billboard'
        if cache.get(key):
            return cache.get(key)[:num]

        url = 'http://www1.billboard.com/rss/charts/hot-100'

        top_list = []
        try:
            data = urllib2.urlopen(url).read()
            soup = BeautifulSoup(data)
            h_list = soup.findAll('item')
            top_list = [cls.parse(item) for item in h_list]
            nodate_item = []
            withdate_item = []
            for item in top_list:
                if item['pub_date']:
                    withdate_item.append(item)
                else:
                    nodate_item.append(item)

            if len(withdate_item) >= 1:
                for item in nodate_item:
                    item['pub_date'] = withdate_item[0]['pub_date']
            else:
                raise Exception('Warning, no date info in Billboard')

            if len(filter(lambda x: x['pub_date']==None, top_list)):
                raise Exception('Warning')

            cache.set(key, top_list, 3600)
            return top_list[:num]
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
            return []
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            return []
