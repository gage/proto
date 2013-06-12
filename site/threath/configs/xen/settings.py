from gulu.configs.common.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

#MEDIA_URL = 'http://media.demo.gd/803BC8/demo_gd_assets/media/'
#MEDIA_URL = 'http://media.demo.gd/media/'
MEDIA_URL = 'http://xen_ip/media/'


ADMIN_MEDIA_PREFIX = '/static/admin/'
DOWNLOAD_DIRECTORY = '/tmp/'

#Stroage
#VIDEO_STREAMER = "rtmp://s1vkz2fohrpgna.cloudfront.net/cfx/st"

### Mobile Session Checking
MOBILE_CHECK_SESSION = True

INSTAGRAM_CLIENT_ID = 'a1f59edf7a4448dbb5ba36b64e923bad'
INSTAGRAM_SECRET = '2a5c6a9aa660471f906cf3bf5f846b57'

### Task Queue
#FILE_SHARING_FOLDER = "S3/share_folder"
#FILE_SHARING_FOLDER_ON_S3 = "share_folder"


# Predefined domain
# SITE_DOMAIN = 'xen_ip'
SITE_DOMAIN = 'xen_ip'
SITE_ID = '4e1717bec770682b6f000021'
# SITE_ID = '5122086dd1c6bf0f6c641c4a'
SITE_PORT = "80"

#Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = True
EMAIL_HOST = '184.105.138.107'
#EMAIL_HOST_USER = 'mailer@gulumail.com'
EMAIL_PORT = 25
SERVER_EMAIL = 'Socialites IM <do.not.reply@socialites.im>'
EMAIL_SUBJECT_PREFIX = '[Socialites IM] '

### DB
DATABASES = {
    'default': {
    	'ENGINE': 'dbindexer',
    	'TARGET': 'mongodb',
        'NAME': 'xen_mongodb_name',
        'TEST_NAME': 'test_xen_mongodb_name',
        'HOST': 'xen_mongo_ips',
    },
    'mongodb': {
    	'ENGINE': 'django_mongodb_engine',
    	'NAME': 'xen_mongodb_name',
    	'TEST_NAME': 'test_xen_mongodb_name',
        'HOST': 'xen_mongo_ips',
    },
}

import jinja2
import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)
JINJA2_ENVIRONMENT_OPTIONS = {
    'bytecode_cache': jinja2.MemcachedBytecodeCache(mc)
}

# Caching
#CACHES = {
#    'default': {
#        'BACKEND' : 'caching.backends.memcached.CacheClass',
#        'LOCATION': '127.0.0.1:11211',
#    }
#}
#CACHE_PREFIX = 'weee:'

REDIS_BACKEND = 'redis://localhost:6379'
CACHE_MACHINE_USE_REDIS = True

#CACHE_MIDDLEWARE_ALIAS = 'default'
#CACHE_MIDDLEWARE_SECONDS = 10
#CACHE_MIDDLEWARE_KEY_PREFIX = ''

#MIDDLEWARE_CLASSES = ('django.middleware.cache.UpdateCacheMiddleware',) + MIDDLEWARE_CLASSES + ('django.middleware.cache.FetchFromCacheMiddleware',)


### HAYSTACK
HAYSTACK_CONNECTIONS = {
   'default': {
       'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
       'URL': 'http://127.0.0.1:8901/solr',
       'DISTANCE_AVAILABLE': True,
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
   },
}

HAYSTACK_REPLICATION_SOLR = True
HAYSTACK_BATCH_SIZE = 4000
HAYSTACK_SOLR_TIMEOUT = 60

### Chat server
CHAT_SERVER_URL = "http://xen_chat_ip:8098"

#GPUB_SERVER = ("xen_chat_ip", 8099)

### MSN
MSN_CLIENT_ID = "00000000480BF797"
MSN_CLIENT_SECRET = "TeuWXvSxenlP9sPiYY8d3uWHyOIat2TD"

# Facebook
FACEBOOK_APP_ID = "315231041827057"
FACEBOOK_APP_SECRET = "7b86dff67b92fb22939d52a1087b421d"
REDIRECT_URI_ACCESS = '/api/oauth_facebook_access'
FACEBOOK_APP_NAMESPACE = "gulu_demo"


### Google App Oauth
GOOGLE_APP_ID = "256347497556-jeoapvin0ju9r8nhf5bg44fdmgjomchu@developer.gserviceaccount.com"
GOOGLE_APP_SECRET = "75wmuISMft1CWXR5ojK5ofir"

# Internal IPs for security
INTERNAL_IPS = ()

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        # 'sentry': {
        #     'level': 'DEBUG',
        #     'class': 'raven.contrib.django.handlers.SentryHandler',
        #     'formatter': 'verbose',
        # },
        # 'console': {
        #     'level': 'DEBUG',
        #     'class': 'logging.StreamHandler',
        #     'formatter': 'verbose'
        # },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        # '': {
        #     'level': 'WARNING',
        #     'handlers': ['sentry'],
        # },
        # 'sentry.errors': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': True,
        # },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        # 'pysolr': {
        #     'level': 'WARNING',
        #     'handlers': ['sentry'],
        #     'propagate': False,
        # },
    },
}
# SENTRY_KEY = 'D16w9w13cr'
# SENTRY_SERVERS = ['http://sentry.demo.gd:9000/store/']



# GeoIP Support
#GEOIP_PATH = '/home/gulu/sites/gulu/repository/data/GeoIP/'
#GEOIP_CITY = "GeoLiteCity.dat"

### LESS
USE_LESS = False

### Clicky tracing code
#CLICKY_SITE_ID="66402226"

### Videos
VIDEO_HOST = "videos.demo.gd.s3.amazonaws.com"

S3_BUCKET_NAME = {
    'video': 'videos.demo.gd',
    'media': 'media.demo.gd'
}
USE_S3 = True

# XMPP
IS_XMPP = True
XMPP_AUTH_KEY = "2vsAATy79N"
XMPP_DOMAIN = 'xen_xmpp_domain'
XMPP_SERVER = XMPP_DOMAIN
XMPP_PUBSUB_HOST = 'xen_pubsub'
XMPP_HTTP_BIND = 'http://xen_ip/http-bind/'

REST_PORT = 5280

XMPP_HTTP_REST = '%s:%s' % (XMPP_DOMAIN, REST_PORT)

WS_PORT = 5279

XMPP_WS_BIND = 'ws://%s:%s/ws-xmpp' % (XMPP_DOMAIN, WS_PORT)

XMPP_MUC_HOST = 'xen_xmpp_muc'
XMPP_ADMIN_JID = "guluxmppadmin@%s" %  XMPP_DOMAIN
XMPP_ADMIN_USER = "guluxmppadmin"
XMPP_ADMIN_PASSWORD = "genie43643"
XMPP_CELERY_QUEUE = True

# if SITE_DOMAIN == 'demo.gulu.com':
# SSL_URLS = (
#     r'/',
# )

USE_REDIS_QUEUE = True

DEVICE_WEBVIEW_MD5 = "_DEVICE_WEBVIEW_MD5_VAR"
DESKTOP_APP_RESOURCE_VERSION = "_DESKTOP_APP_RESOURCE_VERSION_VAR"

# CELERY_DEFAULT_QUEUE = 'default'
# CELERY_ROUTES = {
#     'xmppchat.tasks.trim_uninstall_iphone_app_tokens': {'queue':'w1q'},
#     'search.tasks.process_search': {'queue':'w1q'},
#     'globals.tasks.s3sync_pending_task': {'queue':'w2q'},
#     'movie.tasks.update_movie_data': {'queue':'w2q'},
#     'movie.tasks.update_box_office': {'queue':'w3q'},
#     'movie.tasks.clean_unused_movie_data': {'queue':'w3q'},
# }

DEFAULT_FILE_STORAGE = 's3sync.storage.S3PendingStorage'

AWS_ACCESS_KEY_ID = 'AKIAIIR2TKOBEZ33OGHA'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_UPLOADS = 'media.newdemo.gd'
BUCKET_UPLOADS_URL = 'http://media.newdemo.gd.s3.amazonaws.com/media/'

PRODUCTION = True

CACHES = {
    'default' : {
        'BACKEND' : 'mongo_cache.backend.MongoDBCache',
        'LOCATION': 'socialites_cache',
        'OPTIONS': {
            'DATABASE': 'gulu',
            'HOST': 'xen_mongo_ips',
            'PORT': 27017,
        }
    }
}

if SITE_DOMAIN == "socialites.im":
    try:
        from settings_production import *
    except ImportError:
        pass

