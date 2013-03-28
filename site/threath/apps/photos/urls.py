from django.conf.urls.defaults import *

urlpatterns = patterns('photos.views',
    url(r'^user/(?P<user_id>[\-\.\w]+)/(?P<width>\d+)/(?P<height>\d+)/$', 'get_user_photo_url', name="get-user-photo-url"),
    url(r'^(?P<photo_id>\w+)/download/$', 'download', name="download-photo"),
)

