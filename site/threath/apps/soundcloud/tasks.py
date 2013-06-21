import logging
import globals
from celery.task import task, periodic_task
from celery.schedules import crontab
import datetime

from django.conf import settings

DEFAULT_BILLBOARD_TOP_SONG_NUM = 20

@task
def build_single_ranking_task(ranking, billboard_song):
    from soundcloud.utils import SoundCloudProcessor
    SoundCloudProcessor.build_single_ranking_song(ranking, billboard_song)

@task
def billboard_task():
    from soundcloud.utils import SoundCloudProcessor, DEFAULT_BILLBOARD_TOP_SONG_NUM
    rtn = SoundCloudProcessor.build_top_sounds(DEFAULT_BILLBOARD_TOP_SONG_NUM, is_task=True)

@periodic_task(run_every=crontab(day_of_week='sun,thu', minute=0, hour='0,12'))
def billboard_task_creator():
    """ Periodic task to fetch and create billboard ranking task"""
    billboard_task.delay()
    
