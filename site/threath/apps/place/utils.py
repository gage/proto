import json
import urllib, urllib2

from django.utils.http import urlquote
from django.utils.encoding import smart_str
from django.conf import settings

from place.models import FoursquarePlace

class FoursquarePlaceProcessor(object):
    @classmethod
    def __fs_photo_parse(cls, raw):
        json_data = json.loads(raw)
        photos = []
        for item in json_data['response']['photos']['items']:
            prefix = item['prefix']
            suffix = item['suffix']
            photo = {
                'url': prefix + 'original'  + suffix,
                'thumb': prefix + '300x300'  + suffix,
                'prefix': prefix,
                'suffix': suffix
            }
            photos.append(photo)

        return photos

    @classmethod
    def get_venue_photos(cls, venue_id, limit=200, offset=0):
        cls.FS_PHOTO_URL = "%s%s" % (settings.FOURSQUARE_API_HOST, '/v2/venues/'+venue_id+'/photos')
        para = {
            'client_id': settings.FOURSQUARE_CONSUMER_KEY,
            'client_secret': settings.FOURSQUARE_CONSUMER_SECRET,
            'limit': limit,
            'offset': offset,
            'reasonsDetail': 1,
            'v': '20130620'
        }

        encode_para = urllib.urlencode(para)

        url = '%(fs_photo_url)s?%(para)s' % {
            'para': encode_para,
            'fs_photo_url': cls.FS_PHOTO_URL,
        }

        try:
            data = urllib2.urlopen(url).read()
            photos = cls.__fs_photo_parse(data)
            return photos
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
            return []
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            return []

    @classmethod
    def square_search(cls, sw, ne, q='', limit=20, section=None):
        baseurl  = "https://api.foursquare.com/v2/venues/search"
        para = {
            'sw': sw,
            'ne': ne,
            'query': smart_str(q),
            'limit': limit,
            'client_id': settings.FOURSQUARE_CONSUMER_KEY,
            'client_secret': settings.FOURSQUARE_CONSUMER_SECRET,
            'v': '20130604',
            'intent':'browse'
        }
        url = baseurl + '?' + urllib.urlencode(para)
        print url

        try:
            data = urllib2.urlopen(url).read()
            venues = cls.__fs_search_parse(data)
            return venues
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
            return []
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            return []


    @classmethod
    def __fs_search_parse(cls, raw):
        json_data = json.loads(raw)
        venues = []
        for item in json_data['response']['venues']:

            v = item
            categories = v['categories']
            category = ''
            category_id = ''
            category_plural_name = ''
            category_short_name = ''
            icon_suffix = ''
            icon_prefix = ''
            specials = v['specials']
            contact = v['contact']
            for c in categories:
                if c['primary']:
                    category = c['name']
                    category_id = c['id']
                    category_plural_name = c['pluralName']
                    category_short_name = c['shortName']
                    icon_suffix = c['icon']['suffix']
                    icon_prefix = c['icon']['prefix']
                    break
            fs_venue_model = {
                'fid': v['id'],
                'specials': specials['items'],
                'rating': v.get('rating', 0),
                'tips': item.get('tips', []),
                'lat': v['location']['lat'],
                'lon': v['location']['lng'],
                'address': v['location'].get('address',''),
                'cc': v['location'].get('cc',''),
                'city': v['location'].get('city',''),
                'country': v['location'].get('country',''),
                'state': v['location'].get('state',''),
                'name': v['name'],
                'phone': contact.get('phone'),
                'checkins_count': v['stats'].get('checkinsCount',0),
                'tip_count': v['stats'].get('tipCount',0),
                'users_count': v['stats'].get('usersCount',0),
                'category': category,
                'category_id': category_id,
                'category_plural_name': category_plural_name,
                'category_short_name': category_short_name,
                'icon_suffix': icon_suffix,
                'icon_prefix': icon_prefix,
                '_hd': False
            }
            fs_place = FoursquarePlace(**fs_venue_model)
            venues.append(fs_place)
        fs_ids = [place.fid for place in venues]
        fs_places_in_db = FoursquarePlace.objects.filter(fid__in=fs_ids).values_list('fid', 'id')
        fs_places_dicts = dict((x, y) for x, y in fs_places_in_db)
        for new_place in venues:
            if new_place.fid not in fs_places_dicts.keys():
                new_place.save()
            else:
                new_place.id = fs_places_dicts[new_place.fid]
                # TODO: update field or something
                pass


        return venues


    @classmethod
    def spatial_search(cls, ll, q='', radius=100000, limit=10, section=None):
        baseurl  = "https://api.foursquare.com/v2/venues/explore"

        para = {
            'radius': radius,
            'll': ll,
            'query': smart_str(q),
            'limit': limit,
            'client_id': settings.FOURSQUARE_CONSUMER_KEY,
            'client_secret': settings.FOURSQUARE_CONSUMER_SECRET,
            'v': '20130604',
            'reasonsDetail': 1
        }

        if not q and section:
            para['section'] = section

        url = baseurl + '?' + urllib.urlencode(para)
        try:
            data = urllib2.urlopen(url).read()
            venues = cls.__fs_venue_parse(data)
            return venues
        except urllib2.HTTPError, e:
            print "HTTP error: %d" % e.code
            return []
        except urllib2.URLError, e:
            print "Network error: %s" % e.reason.args[1]
            return []

    @classmethod
    def __fs_venue_parse(cls, raw):
        json_data = json.loads(raw)
        venues = []
        for item in json_data['response']['groups'][0]['items']:

            v = item['venue']
            categories = v['categories']
            category = ''
            category_id = ''
            category_plural_name = ''
            category_short_name = ''
            icon_suffix = ''
            icon_prefix = ''
            specials = v['specials']
            contact = v['contact']
            for c in categories:
                if c['primary']:
                    category = c['name']
                    category_id = c['id']
                    category_plural_name = c['pluralName']
                    category_short_name = c['shortName']
                    icon_suffix = c['icon']['suffix']
                    icon_prefix = c['icon']['prefix']
                    break
            photos = v['photos']
            fs_photo = None
            if photos['count'] is not 0 and len(photos['groups']):
                fs_photo = photos['groups'][0]['items'][0]
            fs_venue_model = {
                'fid': v['id'],
                # 'raw': json.dumps(v),
                'fs_photo': fs_photo,
                'specials': specials['items'],
                'rating': v.get('rating', 0),
                'tips': item.get('tips', []),
                'lat': v['location']['lat'],
                'lon': v['location']['lng'],
                'address': v['location'].get('address',''),
                'cc': v['location'].get('cc',''),
                'city': v['location'].get('city',''),
                'country': v['location'].get('country',''),
                'state': v['location'].get('state',''),
                'name': v['name'],
                'phone': contact.get('phone'),
                'checkins_count': v['stats'].get('checkinsCount',0),
                'tip_count': v['stats'].get('tipCount',0),
                'users_count': v['stats'].get('usersCount',0),
                'category': category,
                'category_id': category_id,
                'category_plural_name': category_plural_name,
                'category_short_name': category_short_name,
                'icon_suffix': icon_suffix,
                'icon_prefix': icon_prefix,
                '_distance': v['location'].get('distance',0)
            }
            fs_place = FoursquarePlace(**fs_venue_model)
            venues.append(fs_place)
        fs_ids = [place.fid for place in venues]
        fs_places_in_db = FoursquarePlace.objects.filter(fid__in=fs_ids).values_list('fid', 'id')
        fs_places_dicts = dict((x, y) for x, y in fs_places_in_db)
        for new_place in venues:
            if new_place.fid not in fs_places_dicts.keys():
                new_place.save()
            else:
                new_place.id = fs_places_dicts[new_place.fid]
                # TODO: update field or something
                pass


        return venues
