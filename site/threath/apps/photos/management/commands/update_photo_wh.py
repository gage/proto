from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import NoArgsCommand
from django.db import connections, models, DEFAULT_DB_ALIAS
from photos.models import Photo


class Command(NoArgsCommand):
    help = "Update photo width and height"
    
    def handle_noargs(self, *args, **options):
        self.stdout.write("This command will update all the photo width and height.\n")
        for photo in Photo.objects.filter(created__gt=datetime(2012, 1, 1)):
            try:
                if photo.image:
                    print photo, photo.image.width, photo.image.height
                    Photo.objects.filter(id=photo.id).update(width=photo.image.width, height=photo.image.height)
            except (IOError, TypeError):
                print 'No file'
                pass
        
        print 'Complete.'
        
