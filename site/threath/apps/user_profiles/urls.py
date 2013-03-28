""" Site user profiles module URLs """

from django.conf.urls.defaults import *
from django.contrib.contenttypes.models import ContentType

from user_profiles.models import UserProfile

urlpatterns = patterns('user_profiles.views',
    url(r'^(?P<user_id>\w+)/$', 'user_main', name="user-profile"),
    url(r'^verify_email/?$', 'verify_email', name="verify-email"),
)

