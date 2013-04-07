import os
import datetime
import uuid
import string

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.db.models.signals import pre_delete
from django.template.loader import render_to_string
from django.template import RequestContext

from utils import get_or_create_user_by_phone
from globals.utils import random_generator


class RegistrationManager(models.Manager):

    '''
    When user clicks the link in a validation email
    We can get the registration object from the activation code which is contained in the activation link
    '''
    def create_registration_obj_for_user(self, user):
        registration = self.create(user=user)
        registration.gen_activation_code()
        return registration

    def get_registration_obj_from_activation_code(self, activation_code):
        try:
            registration = self.get(activation_code=activation_code)
            return registration
        except:
            print "failed to get registration object from activation code"
            return False

    def disable_user_registration_entries(self, user):
        try:
            registrations = self.filter(user=user).delete()
            return True
        except:
            return False


class Registration(models.Model):

    STATUS_NEED_USER_INFO = 1
    STATUS_NEED_VERIFY_EMAIL = 2
    STATUS_COMPLETE = 10

    REG_STATUS = [
        (STATUS_NEED_USER_INFO, "status_need_user_info"),
        (STATUS_NEED_VERIFY_EMAIL, "status_need_email_verified"),
        (STATUS_COMPLETE, "status_complete"),
    ]

    user = models.ForeignKey(User)
    activation_code = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(default=datetime.datetime.now)
    mobile_signup = models.BooleanField(default=False)
    app_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.IntegerField(choices=REG_STATUS, default=STATUS_NEED_USER_INFO, null=True)

    objects = RegistrationManager()

    def __unicode__(self):
        return self.id

    def to_json(self, request=None, detail=False, **kwargs):
        rtn = {
            'id': self.id,
            'user_id': self.user_id,
            'created': self.created
        }
        return rtn

    def need_user_info(self):
        return self.status == Registration.STATUS_NEED_USER_INFO

    def need_email_verify(self):
        return self.status == Registration.STATUS_NEED_VERIFY_EMAIL

    def is_complete(self):
        return self.status == Registration.STATUS_COMPLETE

    def gen_activation_code(self, commit=True):
        #code = self.id+os.urandom(26).encode('hex')
        code = str(uuid.uuid4()).replace('-', '')
        self.activation_code = code
        if commit:
            self.save()

    def send_activation_mail(self):
        '''
        Generate an activation link based on the activation code
        Send the link to the user
        '''

        self.gen_activation_code()

        try:
            activation_url = settings.SITE_DOMAIN + reverse('activate-user', args=[self.activation_code])
            if self.app_name:
                activation_url = '%s?app_name=%s' % (activation_url, self.app_name)
            if (self.mobile_signup is True):
                text_content = r'Hi, visit http://%(activation_url)s to activate your account.' % {'activation_url':activation_url}
                mobile = 1;
            else:
                text_content = render_to_string("email_account_activation.html",{
                    'name': self.user.get_profile().get_display_name(),
                    'activation_url': activation_url,
                    'ssl': settings.SSL
                })
                mobile = 0;

            title = _("Activate your account")
            htmly     = get_template('email_templates/inc_email_activation.html')
            d = Context({ 'addr': activation_url, 'mobile': mobile, 'site_url':settings.SITE_DOMAIN })
            subject, from_email, to = title, 'Account Activation', self.user.email

            html_content = htmly.render(d)

            mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
            mail.attach_alternative(html_content, "text/html")
            mail.send()

            return True
        except Exception as err:
            print 'failed to send activation mail: %s' % err
            return False

    def disable_registration_entry(self):
        '''
        When the registration entry is disabled, user cannot activate his account using this activation code
        '''
        self.status = Registration.STATUS_NEED_VERIFY_EMAIL
        self.activation_code = ""
        self.save()
        return True

    def send_forget_password_mail(self):
        try:
            activation_url = settings.SITE_DOMAIN + reverse('reset-password', args=[self.activation_code])

            title = 'Site password reset letter'
            htmly = get_template('email_templates/inc_email_resetpassword.html')
            d = Context({'addr': activation_url, 'site_url': settings.SITE_DOMAIN})
            subject, from_email, to = title, 'do.not.reply@example.com', self.user.email

            text_content = r'Click this link to reset your password:<a href=http://' + activation_url + r'>Reset password</a>'
            html_content = htmly.render(d)

            mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
            mail.attach_alternative(html_content, "text/html")
            mail.send()

            return True
        except:
            print 'failed to send reset password mail'
            return False


def on_delete_user(sender, **kwargs):
    user = kwargs['instance']
    Registration.objects.filter(user=user).delete()

pre_delete.connect(on_delete_user, sender=User)


class PhoneRegistrationManager(models.Manager):
    def gen_registration_code(self):
        return random_generator(size=6, chars=string.digits)

    def gen_registration_obj(self, phone_sms_e164, country_code):
        user, created = get_or_create_user_by_phone(phone_sms_e164, country_code)
        code = self.gen_registration_code()

        phone_regist, created = self.get_or_create(user=user, defaults={'code': code})
        # Update code
        if phone_regist.code != code:
            phone_regist.update_code(code)
        return phone_regist


class PhoneRegistration(models.Model):

    user = models.ForeignKey(User)
    code = models.CharField(max_length=6)

    # Every time this model be saved
    created = models.DateTimeField(auto_now=True, default=datetime.datetime.now)

    objects = PhoneRegistrationManager()

    def __unicode__(self):
        return self.id

    def activate_user(self):
        self.user.is_active = True
        self.user.save()
        self.delete()

    def update_code(self, code):
        self.code = code
        self.save()

    def send_reg_sms(self):
        msg = "Your actication code is " + self.code
        send_sms(phone_sms_e164=self.user.get_profile().phone_sms_e164, msg=msg)

    def to_json(self, request=None, detail=False, **kwargs):
        rtn = {
            'user_id': self.user_id,
            # 'code': self.code,
            'created': self.created
        }
        return rtn
