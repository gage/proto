import json
import urllib, urllib2

from django.utils.http import urlquote
from django.conf import settings

from place.models import FoursquarePlace

class FoursquarePlaceProcessor(object):
    @classmethod
    def spatial_search(cls, ll, q='', radius=100000, limit=10, section=None):
        cls.FS_SEARCH_URL = "%s%s" % (settings.FOURSQUARE_API_HOST, settings.FOURSQUARE_API_PATH)
        url = '%(fs_search_url)s?venuePhotos=1&radius=%(radius)s&v=20130604&ll=%(ll)s&query=%(q)s&limit=%(limit)s&client_id=%(client_id)s&client_secret=%(client_secret)s' % {
            'radius': radius,
            'fs_search_url': cls.FS_SEARCH_URL,
            'll': ll,
            'q': urlquote(q),
            'limit': limit,
            'client_id': settings.FOURSQUARE_CONSUMER_KEY,
            'client_secret': settings.FOURSQUARE_CONSUMER_SECRET
        }
        if not q and section:
            url += '&section='+section
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
            if photos['count'] is not 0:
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
