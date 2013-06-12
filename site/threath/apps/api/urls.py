from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # (r'^act/', include('api.handlers.act.urls')),
    (r'^auth/', include('api.handlers.auth.urls')),
    # (r'^comments/', include('api.handlers.comments.urls')),
    (r'^facebook/', include('api.handlers.facebook.urls')),
    # (r'^friend_list/', include('api.handlers.friend_list.urls')),
    (r'^globals/', include('api.handlers.globals.urls')),
    # (r'^invite/', include('api.handlers.invite.urls')),
    # (r'^link/', include('api.handlers.link.urls')),
    # (r'^notify/', include('api.handlers.notify.urls')),
    (r'^photos/', include('api.handlers.photos.urls')),
    (r'^registration/', include('api.handlers.registration.urls')),
    # (r'^settings/', include('api.handlers.settings.urls')),
    (r'^sandbox/', include('api.handlers.sandbox.urls')),
    (r'^tag/', include('api.handlers.tag.urls')),
    # (r'^slug/', include('api.handlers.slug.urls')),
    (r'^user/', include('api.handlers.user.urls')),
    (r'^youtube/', include('api.handlers.youtube.urls')),

)

urlpatterns += patterns('django.views.generic.simple',
    url(r'^connect_success/$', 'direct_to_template', {'template': 'connect_end.html'}, name="api-connect-success"),
    url(r'^connect_fail/$', 'direct_to_template', {'template': 'connect_end.html'}, name="api-connect-fail"),
)
