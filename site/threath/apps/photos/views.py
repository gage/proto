""" Site photo module views """
import mimetypes
import os
from django.utils.encoding import smart_str

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from photos.models import Photo

def get_user_photo_url(request, user_id, width, height):
    try:
        user = User.objects.get(pk=user_id)
        photo = user.get_profile().get_display_photo()
    except:
        try:
            user = User.objects.get(username=user_id)
            photo = user.get_profile().get_display_photo()
        except:
            photo = Photo.objects.filter(user_default=True)[0]

    size_str = 'image%sx%s' % (width, height)
    caller = getattr(photo, size_str)

    return HttpResponseRedirect(caller.url)



@login_required
def download(request, photo_id):
    #path = request.GET['path']
    photo = get_object_or_404(Photo, pk=photo_id)
    filename = os.path.basename(photo.image.url)

    wrapper = FileWrapper(open(photo.image.path))
    content_type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type=content_type, stream_content=True)
    response['Content-Length'] = os.path.getsize(photo.image.path)
    response['Content-Disposition'] = "attachment; filename=%s" % smart_str(filename)
    return response













