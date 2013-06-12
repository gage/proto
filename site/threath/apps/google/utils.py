import urllib, urllib2
import json
import gdata.youtube.service
from django.conf import settings
from django.utils.encoding import smart_str

DEVELOPER_KEY = settings.GOOGLE_API_KEY

def _ggl_search_parse(data):
    json_data = json.loads(data)
    response = json_data['responseData']
    results = response['results']
    return results


def google_search(q='', user_ip='127.0.0.1', **more_options):
    uri = "http://ajax.googleapis.com/ajax/services/search/web"
    options = {
        'v': 1.0,
        'q': q,
        'rsz': 8,
        'start': 0,
        'userip': user_ip
    }
    options.update(more_options)
    para = urllib.urlencode(options)
    uri += '?'+para

    try:
        data = urllib2.urlopen(uri).read()
        results = _ggl_search_parse(data)
        return results
    except urllib2.HTTPError, e:
        print "HTTP error: %d" % e.code
        return []
    except urllib2.URLError, e:
        print "Network error: %s" % e.reason.args[1]
        return []
