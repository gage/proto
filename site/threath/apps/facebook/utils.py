from django.contrib.auth import authenticate, login
from django.conf import settings
from api.errors import APIException
import api.errors as api_errors
from httplib2 import Http
from globals.utils import http_request_with_retry
import urllib2, urllib

def login_fb_user(request, facebook_id):
    """ Logs in a User using facebook authentication, returns True 
    if successful, False otherwise """
    auth_user = authenticate(facebook_id=facebook_id)
    if not auth_user:
        return False
    login(request, auth_user)
    return True    


def req_exchange_long_lived_access_token(short_lived_access_token, logger=None):
    params = {  'client_id': settings.FACEBOOK_APP_ID,
                'client_secret': settings.FACEBOOK_APP_SECRET,
                'grant_type': 'fb_exchange_token',
                'fb_exchange_token': short_lived_access_token,
              }
    url = "https://graph.facebook.com/oauth/access_token?%s" % urllib.urlencode(params)

    http_request = Http()

    try:
        resp, content = http_request_with_retry(http_request, url, "GET")
        if resp.get('status') == '400':
            raise APIException(api_errors.ERROR_FACEBOOK_INVALID_TOKEN, resp)
    except socket.error as err:
        if logger:
            logger.info(err)
        return None, None
    else:
        params = content.split('&')
        access_token = params[0].split('=')[1]
        expires = params[1].split('=')[1]
        if logger:
            logger.info("long lived token and expires: %s & %s" % (access_token, expires))        
        return access_token, expires
    