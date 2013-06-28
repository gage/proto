from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/?', include(admin.site.urls)),

    # Groupint the single page app url
    url(r'^$', 'globals.views.home', name="globals-home"),
    url(r'^signup/?', 'globals.views.signup', name="globals-signup"),
    url(r'^login/?', 'globals.views.signup', name="globals-login"),
    url(r'^tpl/(?P<template>.*)', 'globals.views.render_tpl'),
    # url(r'^landing/?$', 'globals.views.home', name="globals-home"),



    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^logout/?$', 'globals.views.globals_logout', name="globals-logout"),

    (r'^api/', include('api.urls')),
    (r'^photos/', include('photos.urls')),
    (r'^registration/', include('registration.urls')),
    (r'^user/', include('user_profiles.urls')),
    (r'^facebook/', include('facebook.urls')),
)


urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
    (r'^.+/?', 'globals.views.home')
)

