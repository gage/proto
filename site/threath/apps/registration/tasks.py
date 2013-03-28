""" Registration Tasks """

__author__ = "Jason Ke <jason.ke@geniecapital.com.tw>"

import globals
from django.conf import settings
from datetime import datetime, timedelta
from celery.schedules import crontab
from celery.task import periodic_task, task
from registration.models import Registration
from django.db.models import Q
from django.contrib.auth.models import User
from slug.models import Slug
from user_profiles.models import UserProfile

@periodic_task(run_every=crontab(minute='*/10'))
def clean_all_expired_users():
    """ Periodic task to clear all expired users(Not activate their account within 15 days) """
    logger = globals.utils.get_logger('delete_inactive_users_celery_task')
    logger.info("Start deleting users...")
    now = datetime.now()
    expiration_datetime = now - timedelta(days = 15)
    expired_users = User.objects.filter(date_joined__lt = expiration_datetime, is_active=False)[:1]
    for user in expired_users:
        try:
            up = user.get_profile()
            up.delete()
        except UserProfile.DoesNotExist as e:
            logger.info("%s" % e)
        Registration.objects.filter(user=user).delete()
        Slug.objects.filter(object_id=user.id).delete()
        user.delete()

    logger.info("Complete...")
