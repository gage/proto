from django.db import models
from django.contrib.auth.models import User

class FacebookProfile(models.Model):
    """ Links a facebook profile to a user """
    user = models.OneToOneField(User, related_name='fb_profile')
    facebook_id = models.CharField(max_length=100, null=True, blank=True)
    access_token = models.CharField(max_length=100)
    fb_flow_token = models.CharField(max_length=100, null=True, blank=True)

    # def __unicode__(self):
    #    return self.user.__unicode__()
