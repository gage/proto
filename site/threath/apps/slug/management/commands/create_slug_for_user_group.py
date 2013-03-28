from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from django.conf import settings
from slug.models import Slug
from group.models import Group



class Command(NoArgsCommand):
    help = "Create user Pubsub Nodes and Subscribe all users"

    def handle_noargs(self, *args, **options):
        self.stdout.write("This script will clean the Slug model and rebuild it.\n")
        go = raw_input("Are you sure you want to do this?  [y/N]: ")
        if go not in 'yY':
            self.stdout.write("Smart move.\n")
            exit()
            
        Slug.objects.all().delete()    
        
        for user in User.objects.all():
            print user.username
            if Slug.objects.filter(object_id=user.pk).count() == 0:
                slug_str = Slug.objects.sluggify(user.username)
                new_slug = Slug(slug=slug_str, content_object=user)
                new_slug.save()
                profile = user.get_profile()
                from user_profiles.models import UserProfile
                UserProfile.objects.filter(id=profile.id).update(slug=new_slug)



        for group in Group.objects.all():
            print group.name
            if Slug.objects.filter(object_id=group.pk).count() == 0:
                if group.is_mutual_group:
                    loop_count = 0
                    for member_id in group.members:
                        if loop_count == 0:
                            user1 = User.objects.get(id=member_id)
                        elif loop_count == 1:
                            user2 = User.objects.get(id=member_id)

                        loop_count = loop_count + 1
                    print user1.username
                    print user2.username
                    if user1.username[0] > user2.username[0]:
                        slug_str = "%s-%s" % (user2.username, user1.username)
                    else:
                        slug_str = "%s-%s" % (user1.username, user2.username)
                else:
                    slug_str = Slug.objects.sluggify(group.name)
                new_slug = Slug(slug=slug_str, content_object=group)
                new_slug.save()
                group.slug = slug_str
                group.save()

                
