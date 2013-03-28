# Query
from django.db.models import Q
	Q(question__startswith='Who') | Q(question__startswith='What')

# Redirect
return HttpResponseRedirect(slugreverse(request.user, "user-profile", args=[request.user.id]))

# Dynamic Folder
import os
import hashlib
def get_photo_upload_path(instance, filename):
    name_hash = hashlib.md5(filename).hexdigest()
    return os.path.join('photos',name_hash[0:2], name_hash[2:4], name_hash[4:6], name_hash[6:8], filename)