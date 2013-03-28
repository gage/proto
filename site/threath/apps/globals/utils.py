# # -*- coding: utf-8 -*-

import datetime
import HTMLParser
import json
import logging
import math
import oauth2
import os
import pickle
import pretty
import re
import random
import string
import threading
import time
import urllib2, urllib
import uuid

from PIL import Image

from haystack import connections as haystack_connections
from haystack.constants import DEFAULT_ALIAS

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.files import File
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape

from decorators import retry


MONGO_PK = re.compile(r'[a-fA-F0-9]{24}')


# # If there is something we want to broadcast to user, we can add message here.
# SYSTEM_MESSAGE = ""
# SYSTEM_TITLE = "techcrunch_disrupt"

HOME_HTML = "home_html"
MOBILE_HTML = "mobile_html"

http_url_re = r'((http|https)\://)?(?#Username:Password)(?:\w+:\w+@)?(?#Subdomains)(?:(?:[-\w]+\.))+(?#TopLevel Domains)(?:(com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2})\b)(?#Port)(?::[\d]{1,5})?(?#Directories)(?:(?:(?:\/(?:[-\w~!@%$+|.,=]|%[a-f\d]{2})+)+|\/)+|\?|#)?(?#Query)(?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=?(?:[-/\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-/\w~!$+|.,*:]|%[a-f\d{2}])+=?(?:[-/\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?#Anchor)(?:#(?:[-\?/\w~!$+|.,*:=]|%[a-f\d]{2})*)?'


#=======================
# logger setup
#=======================
LOG_DIR = os.path.join(settings.SITE_ROOT, 'log')

#===========================================================================
# Create directory for log
#===========================================================================
try:
    os.makedirs(LOG_DIR)
except:
    """
    the directory has been existed.
    """
    pass


def is_mongo_pk(s):
    try:
        return MONGO_PK.match(s)
    except TypeError:
        return False


# === Checked ===
def slugreverse(user, viewname, urlconf=None, args=None, kwargs=None, current_app=None):
    """ Reverses a view to a slug-based URL for user pages.

    Args:
        user: django User obj

        For other arguments see the django.core.urlresolvers.reverse

    Returns:
        A slug-based URL.
    """
    url = reverse(viewname, urlconf, args, kwargs, current_app)
    if not user.get_profile().slug:
        from slug.models import Slug
        slug, created = Slug.objects.get_or_create(slug=user.username, defaults= {'content_object': user})
        user.get_profile().slug = slug
        user.get_profile().save()

    return "/%s/%s" % (user.get_profile().slug.slug, "/".join(url.split("/")[3:]))

# # =================== Haystack =====================

def get_index(model):
    unified_index = haystack_connections[DEFAULT_ALIAS].get_unified_index()
    index = unified_index.get_index(model)
    return index


def get_search_backend():
    return haystack_connections[DEFAULT_ALIAS].get_backend()


def get_django_ct(content_type):
    if not content_type:
        return None
    django_ct = '%s.%s' % (content_type.app_label, content_type.model)
    return django_ct


def create_fake_user_with_email(email):
    if User.objects.filter(email=email).exists():
        return False

    email_front = email.split('@')[0]
    username = make_username(email_front)

    user = User.objects.create_user(username, email)
    user.is_active = False
    user.save()

    user_profile = user.get_profile()
    user_profile.nickname = email_front
    user_profile.save()

    return user


def bigpipe_pagelet(pagelet_func):
    """
    generate pagelet string to send to browser
    """
    def _decorated(*args, **kwargs):
        paglet_rtn = pagelet_func(*args, **kwargs)
        bigpipe_json = {'id': paglet_rtn[0],
                        'innerHTML': paglet_rtn[1],
                        'jsModuleFile': paglet_rtn[2],
                        'css_files': paglet_rtn[3]
                        }
        if settings.DEBUG:
            bigpipe_json['css_files'] = []
        return '<script type="text/javascript">BigPipe.onArrive(%s);</script>' % json.dumps(bigpipe_json)
        
    return _decorated

    
def get_logger(logger_name, path_to_log_file=None, level=logging.DEBUG):
    """
    Multiple calls to getLogger() with the same name will always return a reference to the same Logger object.
    """
    logger = logging.getLogger(logger_name)
    
    if not path_to_log_file:
        path_to_log_file = os.path.join( LOG_DIR, logger_name + ".log" )
    
    if not logger.handlers:
        file_handler = logging.handlers.RotatingFileHandler(path_to_log_file,
                                                   mode='a', 
                                                   maxBytes=104857600,
                                                   backupCount=10
                                                   )
        
        formatter = logging.Formatter(fmt='%(levelname)s: ===== %(asctime)s.%(msecs)d ====\n%(message)s\n',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(level)
    
    return logger

def strip_http_protocol(raw_string):
    return re.sub("https?://", "", raw_string)
    
def url_html_decorator(rawString, autoescape=False):
    """ This function wraps all http urls within rawString with HTML anchor tag and return the manipulated string.

    Example:
        case 1:
            rawString = "abc http://example.com def"    
            =>
            "foo <a href="http://example.com" class="url_html_decorator" target="_blank">http://example.com</a> bar"
        
        case 2:
            rawString = "foo http://example.com (Hello, Site!) bar    
            =>
            "foo <a href="http://example.com" class="url_html_decorator" target="_blank">Hello, Site</a> bar"
    """
    
    if not rawString:
        return rawString
    
    #print "rawString: %s" % rawString 
    rawString = rawString.replace("&amp;", "&")
    
    target = r'(\s\([^\n^)]*\))?'
    #rule = http_url_re + http_url_2_re + target
    rule = http_url_re + target  
    
    parser = re.compile(rule)
    
    def decorator(matchObj):
        
        tokens = matchObj.group(0).split(' ', 1)
        
        #print "tokens: %s" % tokens
        
        if len(tokens) == 1:
            target = re.sub("(http://|https://)", "", urllib.unquote( str(tokens[0]) ).decode('utf-8'))
            #print "target: %s" % target
            
        else:
            target = tokens[1].strip('()')
            target = target.replace('<', '&lt').replace('>', '&gt').replace('"', '&quot') 
        
        #print "target: %s" % target
        
        http_protocol = "http://"
        url = tokens[0]
        #print "url: %s" % url
        
        result = re.search("(https|http)", url)

        if not result:
            old_url = url
            url = http_protocol + url

        #disable url validation according to performance issue while fetching social stream list.
#            validate = URLValidator(verify_exists=True)
#            try:
#                validate(url)
#            except ValidationError as err:
#                #print "old_url: %s" % old_url
#                return old_url
        
        return "<a href='" + url + "' class='http_url_decorator' target='_blank'>" + target + "</a>"
    
    if autoescape:
        rawString = escape(rawString)
    
    return parser.sub( decorator, rawString )

def get_pretty_datetime_format(datetime_or_utc_sec):
    
    if isinstance(datetime_or_utc_sec, datetime.datetime):
        ts = datetime_or_utc_sec
    else:
        ts = datetime.datetime.fromtimestamp(float(datetime_or_utc_sec))
    
    now = datetime.datetime.now()
    delta = now - ts
    if delta.days > 1:
        month = ts.strftime('%h')
        day = str(ts.day).lstrip('0')
        year = str(ts.year)
        
        since = "%s %s, %s" % (month, day, year)
    else:
        since = pretty.date(now-delta) 
        
        if delta.days > 0:
            hour = ts.strftime("%I").lstrip('0')
            minute = ts.strftime("%M")
            locale = ts.strftime("%p").lower()
            
            time_str = "%s:%s%s" % (hour, minute, locale) 
            since = since.title() + " at " + time_str    
    
#     return since

@retry(Exception, tries=2, delay=2, backoff=2, logger=None)
def urlopen_with_retry(url, timeout):
    resp =  urllib2.urlopen(url, timeout=timeout)
    return resp

@retry(Exception, tries=5, delay=3, backoff=2, logger=None)
def http_request_with_retry(http_requester, url, method, params=None, headers=None):
    if params and headers:
        resp, content = http_requester.request( url, method, params, headers=headers )
    elif params:
        resp, content = http_requester.request( url, method, params )
    elif headers:
        resp, content = http_requester.request( url, method, headers=headers)
    else:
        resp, content = http_requester.request( url, method )
    return resp, content     

def fetch_image_from_url(image_url, alter_name=None, update_photo=None, logger=None):
    
    if not image_url:
        return None
    
    if not logger:
        logger = get_logger('fetch_image_from_url', level=logging.DEBUG) 
    
    try:
        if update_photo:
            photo_id = update_photo.id
        else:
            photo_id = ""
        logger.info("Fetching photo id: %s, image_url: %s" % (photo_id, image_url))

        filename = alter_name if alter_name else str(uuid.uuid4()) + "_" + os.path.basename(image_url)
        url_utf8 = image_url.encode("utf8")

        logger.debug("url_utf8: %s" % url_utf8)

        try:
            response = urlopen_with_retry(url_utf8, 30)
        except urllib2.HTTPError as http_err:
            logger.info("urlopen-HTTPError: " + str(http_err))
            return None
        except Exception as err:
            logger.info("urlopen-UnknownError: " + str(err))
            return None
        else:
            headers = response.headers
            maintype = headers.maintype
            subtype = headers.subtype
            
            logger.debug("maintype:%s" % maintype)
            logger.debug("subtype:%s" % subtype)

            if maintype and maintype == 'image':
                img_format = subtype

                if img_format == "*":
                    img_format = "jpeg"

                path_to_file = settings.MEDIA_ROOT + '/photos/' + filename
                logger.debug("path_to_file: %s" % path_to_file)
                #===============================================================================
                # write file
                #===============================================================================
                img = open( path_to_file, 'w' )
                img.write( response.read() )
                img.close()
                
                logger.debug("img: %s" % img)
                
                #=======================================================================
                # verify photos
                #=======================================================================
                try:
                    image = Image.open(path_to_file)
                    logger.info("image: %s" % image)
                    image.verify()
                except IOError as io_err:
                    logger.info( "Image.open-IOError: " + str(io_err) )
                    return None
                except Exception as err:
                    logger.info( "Image.open-UnknownError: " + str(err) )
                    return None
                else:
                    target_file = File(open(path_to_file))
                    logger.debug("target_file: %s" % target_file)
                    
                    photo = update_photo
                    photo.image.save(filename, target_file, save=True)
                    logger.debug("photo: %s" % photo.__dict__)
                    return photo
            else:
                return None
    except Exception as err:
        logger.info( str(err) )
        return None
    else:
        return None

# def findnth(haystack, needle, n): 
#     parts= haystack.split(needle, n+1)
#     if len(parts)<=n+1:
#         return -1
#     return len(haystack)-len(parts[-1])-len(needle)


# def _build_default_photo(photo_filename, default_field):
#     from photos.models import Photo
#     img_fallback = '%s/photos/%s' % (settings.MEDIA_ROOT, photo_filename)
#     try:
#         image = Image.open(img_fallback)
#         image.verify()
#         photo = Photo(** {default_field: True})
#         photo.save()
#         Photo.objects.filter(pk=photo.pk).update(image='photos/' + photo_filename)
#         photo = Photo.objects.get(pk=photo.pk)
#         return photo

#     except:
#         img_fallback = '%s/images/%s' % (settings.GLOBALS_STATIC_ROOT, photo_filename)
#         image = Image.open(img_fallback)
#         image.verify()
#         target_file = File(open(img_fallback))
#         photo = Photo(** {default_field: True})
#         photo.image.save(photo_filename, target_file, save=True)
#         return photo


def get_users_display(model, user_ids, format_type=None):
    def _get_last_sender(user_ids):
        try:
            return User.objects.get(id=user_ids[-1])
        except User.DoesNotExist:
            print 'user has been deleted'
            return None

    def _get_last_two_senders(user_ids):
        if len(user_ids) < 2:
            raise Exception
        else:
            return User.objects.filter(id__in=user_ids[-2:])

    if len(user_ids) == 1:
        user = _get_last_sender(user_ids)
        # TODO
        # Automatic fault correction
        if not user:
            model.delete()
            return ''

        if format_type == HOME_HTML:
            return '<span class="highlight">%s</span>' % user.get_display_name()
        else:
            return user.get_display_name()
    elif len(user_ids) == 2:
        users = _get_last_two_senders(user_ids)
        if len(users) < 2:
            model.delete()
            return ''

        if format_type == HOME_HTML:
            return _('<span class="highlight">%(user1)s</span> and <span class="highlight">%(user2)s</span>') % {'user1': users[0].get_display_name(), 'user2': users[1].get_display_name()}
        else:
            return _('%(user1)s and %(user2)s') % {'user1': users[0].get_display_name(), 'user2': users[1].get_display_name()}
    else:
        users = _get_last_two_senders(user_ids)
        if len(users) < 2:
            model.delete()
            return ''

        if format_type == HOME_HTML:
            return _('<span class="highlight">%(user1)s</span>, <span class="highlight">%(user2)s</span> and <span class="highlight">%(remain_user)s</span> other friends') % {
                'user1': users[0].get_display_name(),
                'user2': users[1].get_display_name(),
                'remain_user': len(user_ids) - 2
            }
        else:
            return _('%(user1)s, %(user2)s and %(remain_user)s other friends') % {
                'user1': users[0].get_display_name(),
                'user2': users[1].get_display_name(),
                'remain_user': len(user_ids) - 2
            }

def super_truncatesmart(value, limit=30):
    """
    Truncates a string after a given number of chars keeping whole words.
    
    Usage:
        {{ string|super_truncatesmart }}
        {{ string|super_truncatesmart:50 }}
    """
    
    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value
    
    # Make sure it's unicode
    value = unicode(value)
    
    words = value.split(' ')
    space_count = float(len(words))
    char_count = float(len(value))
    
    if char_count == 0:
        return value
    
    if space_count/char_count > 0.13:
        """ english """
        if space_count <= limit:
            return value
        return ' '.join(words[:limit]) + ' ...'
    else:
        """ chinese """
        if char_count <= limit*2.5:
            return value
        return value[:int(limit*2.5)] + ' ...'

def check_facebook_profile(user, check_if_expired=False):
    try:
        profile = user.fb_profile

    except FacebookProfile.DoesNotExist:             
        return False
    else:
        if check_if_expired:
            return not profile.is_expired
        else:
            return True

def check_instagram_profile(user):
    try:
        profile = user.instagram_profile
    except InstagramProfile.DoesNotExist:                        
        return False
    else:
        return  True    

def check_foursquare_profile(user):
    try:
        profile = user.foursquare_profile
    except FoursquareProfile.DoesNotExist:                        
        return False
    else:
        return True    

def check_twitter_profile(user):
    try: 
        profile = user.twitter_profile            
    except TwitterProfile.DoesNotExist:
        return False
    else:
        return True

def mk_int(s):
    if type(s) == type(int()):
        return s
    else:
        s = s.strip()
        return int(s) if s else 0

def random_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def get_page(url, params_dict={}, oauth2_params_dict={}):
    '''
    Get the page content of url with parameters params_dict
    '''
    page_content = ''
    params = ''
    if params_dict:
        params = urllib.urlencode(params_dict)
    url = "%s?%s" % (url, params)
    if oauth2_params_dict:
        CONSUMER_KEY = oauth2_params_dict['CONSUMER_KEY']
        CONSUMER_SECRETE = oauth2_params_dict['CONSUMER_SECRETE']
        TOKEN = oauth2_params_dict['TOKEN']
        TOKEN_SECRETE = oauth2_params_dict['TOKEN_SECRETE']

        consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRETE)
        oauth_request = oauth2.Request('GET', url, {})
        oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                            'oauth_timestamp': oauth2.generate_timestamp(),
                            'oauth_token': TOKEN,
                            'oauth_consumer_key': CONSUMER_KEY})

        token = oauth2.Token(TOKEN, TOKEN_SECRETE)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
        url = oauth_request.to_url() # Generate signed url
    

    headers = {
        'Accept-Charset': 'UTF-8,*',
        'User-Agent': ' Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20100101 Firefox/16.0',
        'Accept-Language': 'en-US,zh-TW',
    }
    req = urllib2.Request(url, headers = headers)
    res = urllib2.urlopen(req)
    page_content = res.read()
    try:
        page_content = page_content.decoded('utf-8')
    except (AttributeError,UnicodeDecodeError) as e:
        pass
        
    return page_content

def latlon_to_city(latlon=''):
    if latlon:
        params_dict = {
            'latlng': latlon,
            'sensor': 'true',
        }
        url = 'http://maps.googleapis.com/maps/api/geocode/json'
        data = get_page(url, params_dict=params_dict)
        json_data = json.loads(data)        
        rtn = None
        if json_data['status']=='OK':
            try:
                rtn = json_data['results'][0]['address_components'][2]['short_name']
            except (IndexError, KeyError) as e:
                print "Exception %s" % e
    return rtn

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def html_entity_decode(s):
    h = HTMLParser.HTMLParser()
    return h.unescape(s)

def random_sleep(max_seconds=10):
    random.seed()

    n = random.random() * max_seconds
    print "sleep for %s seconds " % n
    time.sleep(n)

    return True
