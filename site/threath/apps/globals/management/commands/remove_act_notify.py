from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import NoArgsCommand
from django.db import connections, models, DEFAULT_DB_ALIAS
from django.db.models import F, Q
from act.models import Action
from notify.models import Notify


class Command(NoArgsCommand):
    help = "Remove all action and notification"
    
    def handle_noargs(self, *args, **options):
        Notify.objects.all().delete()
        Action.objects.all().delete()
        
        print 'Complete.'
        
