""" Site facebook views """

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect

from facebook.facebook_api import FacebookAPI
from facebook.graph_api import get_user_from_cookie
from facebook.utils import login_fb_user

FB_LOGIN_REDIRECT = '/home/'


def connect(request):
    """ Facebok-based signup/login.  Will try the following in order:
    
    1.  If this is an existing user, log them in and redirect.
    2.  If we can attach this fb user to an existing user by email, create a local FacebookProfile,
        log them in and redirect.
    3.  If we can create a user with the email address and username given, create the user, create a
        local FacebookProfile, log them in and redirect.
    4.  Ask the user for their username, creates a new user, etc.
    """
    fb_user = get_user_from_cookie(request.COOKIES, 
        settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET)
    if not fb_user:
        return redirect('registration-signup')
    fb = FacebookAPI(fb_user['access_token'])
    
    # make sure the token is actually valid
    if not fb.is_authenticated():
        return redirect('registration-signup')
    
    fb_profile = fb.get_profile()
    fb_local_profile = fb.get_local_profile()
    
    # Case 1, existing user
    if fb_local_profile is not None:
        # we're already attached to a site user so log them in and redirect
        login_fb_user(request, fb_local_profile.facebook_id)
        return redirect(FB_LOGIN_REDIRECT)
    
    # Case 2, try to attach to an existing profile
    fb_email = fb_profile['email']
    try:
        user = User.objects.get(email=fb_email)
        fb_profile = fb.create_local_profile(user)
        login_fb_user(request, fb_profile.facebook_id)
        return redirect(FB_LOGIN_REDIRECT)
    except User.DoesNotExist:
        pass    
    try:
        user = User.objects.get(username=fb_email)
        fb_profile = fb.create_local_profile(user)
        login_fb_user(request, fb_profile.facebook_id)
        return redirect(FB_LOGIN_REDIRECT)
    except User.DoesNotExist:
        pass
    # Case 3, see if username is OK    
    try:
        fb_username = fb_profile['username']
    except KeyError:
        try:
            fb_username = fb_profile['email'].split('@')[0]
        except:
            fb_username = None
    if not fb_username:
        fb_username = None
    
    user_exist = User.objects.filter(username=fb_username).exists()
    serial = 0
    origin_username = fb_username
    while user_exist:
        fb_username = '%s%s'%(origin_username, serial)
        user_exist = User.objects.filter(username=fb_username).exists()
    user = fb.create_user(fb_username, fb_email)
    login_fb_user(request, fb_profile['id'])
    return redirect(FB_LOGIN_REDIRECT)
            