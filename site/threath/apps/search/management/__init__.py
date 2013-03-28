from django.conf import settings
from django.db.models import signals

import search.models as search_models

def create_default_city(sender, **kwargs):
    print 'We can use "signals.post_syncdb.connect" to do thing after syncdb!'


signals.post_syncdb.connect(create_default_city, sender=search_models,
    dispatch_uid="search.management.create_default_city")
