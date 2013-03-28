from django.db.models import signals
from django.contrib.auth.models import User

from globals import models as global_models

def create_anonymous_user(sender, **kwargs):
    """ Creates anonymous User instance. """
    try:
        User.objects.get(username="AnonymousUser")
    except User.DoesNotExist:
        User.objects.create(username='AnonymousUser')
    except User.MultipleObjectsReturned:
        for u in User.objects.filter(username="AnonymousUser")[1:]:
            u.delete()

def create_xmpp_admin(sender, **kwargs):
    try:
        User.objects.get(username="sitexmppadmin")
    except User.DoesNotExist:
        User.objects.create(username='sitexmppadmin')
    except User.MultipleObjectsReturned:
        for u in User.objects.filter(username="sitexmppadmin")[1:]:
            u.delete()

signals.post_syncdb.connect(create_anonymous_user, sender=global_models,
    dispatch_uid="globals.management.create_anonymous_user")
