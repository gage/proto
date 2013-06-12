import urllib
import gdata.youtube.service
from django.conf import settings
from django.utils.encoding import smart_str

DEVELOPER_KEY = settings.GOOGLE_API_KEY

PARSE_STANDARD = 'standardfeeds'
PARSE_SEARCH = 'search'

def _parse_youtube_id(entry, parse_type=PARSE_STANDARD):
    if parse_type=='standardfeeds':
        for e in entry.media.extension_elements:
            if e.tag == 'videoid':
                return e.text
    elif parse_type=='search':
        return entry.id.text.split('/')[-1]
    return None

def _parse_youtube_thumbnail(entry):
    thumbnail = ''
    for thumb in entry.media.thumbnail:
        if thumb.url:
            thumbnail = thumb.url
            break
    return thumbnail

def _get_yt_service():
    yt_service = gdata.youtube.service.YouTubeService()
    yt_service.developer_key = DEVELOPER_KEY
    return yt_service

def _parse_entry(entry, parse_type=PARSE_STANDARD):
    youtube_id = _parse_youtube_id(entry, parse_type=parse_type)
    return {
        'title': entry.media.title.text,
        'duration': entry.media.duration.seconds,
        'view_count': entry.statistics.view_count,
        'youtube_id': youtube_id,
        'thumburl': 'https://i.ytimg.com/vi/%s/%sdefault.jpg' % (youtube_id, 'hq')
    }

def fetch(youtube_id):
    yt_service = _get_yt_service()
    entry = yt_service.GetYouTubeVideoEntry(video_id=youtube_id)
    return _parse_entry(entry, PARSE_SEARCH)
   
def youtube_search(geo_code='TW', category='most_viewed', **more_options):
    options = {'time': 'today'}
    options.update(more_options)

    yt_service = _get_yt_service()
    yt_list = []
    rtn = []

    # Query
    parse_type = ''
    if options.get('q'):
        parse_type = PARSE_SEARCH
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = smart_str(options.get('q'))
        query.orderby = 'viewCount'
        query.racy = 'include'
        yt_list = yt_service.YouTubeQuery(query)
    else:
        parse_type = PARSE_STANDARD
        uri = 'http://gdata.youtube.com/feeds/api/standardfeeds/%(geo_code)s/%(category)s' % {
            'geo_code': geo_code,
            'category': category
            }

        para = urllib.urlencode(options)
        if para:
            uri += '?'+para
        yt_list = yt_service.GetYouTubeVideoFeed(uri)

    for entry in yt_list.entry:
        obj = _parse_entry(entry, parse_type)
        rtn.append(obj)
    
    return rtn
