from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from datetime import timedelta, datetime

class Command(NoArgsCommand):

    def handle_noargs(self, *args, **options):
        self.stdout.write("This command will clean up the guest accounts which havn't logged in since two weeks ago.\n")
        submit = raw_input("Are you sure you want to do this?  [y/N]: ")
        if submit in 'yY':
            User.objects.filter(is_guest=True, last_login__lt=datetime.now()-timedelta(days=14)).delete()
        else:
            pass

