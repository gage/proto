import os
import datetime
import logging

from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from registration.models import Registration
from django.db.models import Q

class Command(BaseCommand):
    #Sample Commands:
    def handle(self, *args, **options):
        self.stdout.write("Registration Utility.\n")
        logger = logging.getLogger('registration')
        if len(args) >= 1:
            if args[0]=='clean_expired_users':
                #Get the registration objects that are over 15 days and not in complete state
                expire_datetime = datetime.datetime.now() - timedelta(days=15)
                reg_objs = Registration.objects.filter(Q(created__lt=expire_datetime) & ~Q(status=Registration.STATUS_COMPLETE))
                for reg_obj in reg_objs:
                    try:
                        logger.info("Deleting expired user %s" % reg_obj.user)
                        reg_obj.user.delete()
                    except Exception as e:
                        logger.debug(e)
                