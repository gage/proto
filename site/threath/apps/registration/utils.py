import threading
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _
from django.template.loader import get_template
from django.template import Context

from slug.models import Slug
from globals.utils import random_generator


def send_invite_email(from_user, to_email, use_thread=True):
    try:
        site_url = settings.SITE_DOMAIN
        account_name = from_user.get_profile().get_display_name()
        title = _('%(account)s is inviting you to example.com!!') % {'account':account_name}
        msg = _('Join and have fun!!<br/> Just check <a href="http://%(addr)s">example.com</a>')% {'addr': site_url}
        htmly = get_template('email_templates/inc_email_invite_site.html')
        d = Context({'title':title, 'msg': msg, 'site_url':settings.SITE_DOMAIN, 'account_name':account_name })
        subject, from_email, to = title, 'do.not.reply@example.com', to_email

        html_content = htmly.render(d)

        mail = EmailMultiAlternatives(subject, msg, from_email, [to])
        mail.attach_alternative(html_content, "text/html")
        if use_thread:
            threading.Thread(target=mail.send).start()
        else:
            mail.send()
        return True
    except:
        print 'Failed to send invitation mail'
        return False


def sign_up(username, password, request):
    """ Processes a new signup. And returns the created user object. """
    from registration.models import Registration

    user = User(
        username=username,
    )

    user.set_password(password)
    user.is_active = False
    user.save()

    registration = Registration.objects.create_registration_obj_for_user(user=user)

    return user


def check_username(name):
    """ Returns True is a username is valid and available, False otherwise. """
    return Slug.objects.validate(name)


def make_username(seed="user"):
    """ Generates a valid, unique username from `seed`. """
    from globals.utils import u_slugify
    seed = u_slugify(seed)

    if check_username(seed):
        return seed

    postfix = 1
    while not check_username("%s%s" % (seed, postfix)):
        postfix += 1

    return "%s%s" % (seed, postfix)


def create_new_user():
    def _gen_username():
        username = '_' + random_generator(size=7, chars=string.lowercase + string.digits)
        return username

    def _gen_password():
        password = random_generator(size=6, chars=string.lowercase + string.digits)
        return password

    username = _gen_username()

    while User.objects.filter(username=username).exists():
        username = _gen_username()

    email = username + '@example.com'
    system_gen_password = _gen_password()
    user = User.objects.create_user(username, email, system_gen_password)
    user.is_active = False
    user.save()
    user.get_profile().system_gen_password = system_gen_password
    user.get_profile().save()

    return user


def get_or_create_user_by_phone(phone_sms_e164, country_code):
    from user_profiles.models import UserProfile
    created = False

    # User already exists
    if UserProfile.objects.filter(phone_sms_e164=phone_sms_e164).exists():
        user_profile = UserProfile.objects.get(phone_sms_e164=phone_sms_e164)
        created = False
        return user_profile.user, created

    created = True
    user = create_new_user()
    profile = user.get_profile()
    profile.phone_sms_e164 = phone_sms_e164
    profile.phone_sms = phone_sms_e164
    profile.country_code = country_code
    # TODO: Gen password
    profile.save()

    return user, created
