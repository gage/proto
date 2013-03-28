import random
import string


from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete


class SlugManager(models.Manager):
    """
    Slug manager
    """

    MINLENGTH = 3
    MAXLENGTH = 15

    """
    check if input_str is a valid slug
    """
    def validate(self, input_str):
        input_str.lower()

        if " " in input_str:
            return False

        #check contain '-'
        if "-" in input_str:
            return False

        #check length
        if len(input_str) > self.MAXLENGTH or len(input_str) < self.MINLENGTH:
            return False

        #check if is restricted
        if input_str in settings.SLUG_RESTRICTED_KEYWORDS:
            return False

        #check existence
        exisit_count = self.filter(slug=input_str).count()
        if exisit_count > 0:
            return False

        #check if is username
        #username_count = User.objects.filter(username=input_str).count()
        #if username_count > 0:
        #    return False

        return True


    '''
    return a string that is valid for slug
    '''
    def sluggify(self, input_str):
        input_str = input_str.replace('-', '_')
        input_str = input_str.replace(' ', '_')
        input_str = input_str.lower()

        if len(input_str) < self.MINLENGTH:
            n = self.MINLENGTH-len(input_str)
            random_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(n))
            input_str = '%s%s' % (input_str, random_str)

        elif len(input_str) > 15:
            input_str = input_str[:15]

        original = input_str
        postfix = 1
        while not self.validate(input_str):
            input_str = "%s%s" % (original, postfix)

            if len(input_str) > 15:
                input_str = "%s%s" % (original[:30 - len(input_str)], postfix)

            postfix = postfix + 1

        return input_str

    def genRandomSlugString(self, length):

        if length > 15 or length < 5:
            return False
        characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        string = ''
        for i in range(length):
            string = '%s%s' % (string, characters[random.randint(0, len(characters)-1)])

        return string

class Slug(models.Model):
    """
    model for object slug
    """
    content_type = models.ForeignKey(ContentType, null=False, blank=False)
    content_object = GenericForeignKey('content_type', 'object_id')
    object_id = models.CharField(max_length=24, blank=True, null=True)
    slug = models.CharField(max_length=15, blank=True, null=True)
    change_count = models.IntegerField(default=0)
    objects = SlugManager()

    def change_slug_name(self, input_str, ignore_change_count=False):
        if input_str == self.slug:
            return True

        if self.change_count < 3 and Slug.objects.validate(input_str):
            self.slug = input_str
            if (not ignore_change_count):
                self.change_count = self.change_count + 1
            self.save()
            
            return True
        else:
            return False

    def __unicode__(self):
        return self.slug

def on_delete_user(sender, **kwargs):
    print 'pre delete user in slug'
    user = kwargs['instance']
    Slug.objects.filter(object_id=user.id).delete()
    
pre_delete.connect(on_delete_user, sender=User)



