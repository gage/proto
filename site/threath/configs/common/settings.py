# Django settings for threath project.

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

# EXT:
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

MANAGERS = ADMINS
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'dbindexer',
        'TARGET': 'mongodb',
        'NAME': 'threath',
        'TEST_NAME': 'test_threath',
    },
    'mongodb': {
        'ENGINE': 'django_mongodb_engine',
        'NAME': 'threath',
        'POST': 8000,
        'TEST_NAME': 'test_threath',
    },
}

DBINDEXER_SITECONF = 'threath.configs.common.dbindexes'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
# TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Asia/Taipei'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = ''

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'dfvbqa_xar0vrpc1nor-0v+58e&%nn33w)737chmf$)#^jde8j'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
    'coffin.template.loaders.Loader',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}


import jinja2
JINJA2_ENVIRONMENT_OPTIONS = {
    'bytecode_cache': jinja2.FileSystemBytecodeCache(os.path.join(SITE_ROOT, 'configs/common/jinja_cache'), '%s.cache')
}

JINJA2_TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

JINJA2_DISABLED_APPS = (
    'admin',
    'comments',
    'imagekit',
)

JINJA2_EXTENSIONS = (
    'jinja2.ext.autoescape',
)

MIDDLEWARE_CLASSES = (
    'autoload.middleware.AutoloadMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'globals.middleware.SlugURLMiddleware',
)

### Authentication
AUTHENTICATION_BACKENDS = (
    'user_profiles.auth_backends.UserProfileBackend',
    'facebook.auth_backends.FacebookBackend',
    'globals.auth_backends.SessionBackend',
    'globals.auth_backends.CaseInsensitiveModelBackend',
)

ROOT_URLCONF = 'threath.configs.common.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
    os.path.join(SITE_ROOT, 'static', 'css')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.comments',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'autoload',
    'coffin',
    'dbindexer',
    'djangotoolbox',
    'imagekit',
    'haystack',
    'mongo_cache',
    'diff_match_patch',
    # 'djcelery',
    # 'phonenumbers',

    'api',
    'facebook',
    # 'gcomments',
    'globals',
    # 'invite',
    # 'link',
    # 'notify',
    'photos',
    'place',
    # 'phonefix',
    'registration',
    'search',
    'slug',
    'soundcloud',
    # 'testing',
    'user_profiles',
    'youtube',
)


### Google
GOOGLE_API_KEY = 'AIzaSyCAIoKgWrtOHRXXNWVslzMGLcOTqCjlnTk'

### Foursquare
FOURSQUARE_API_HOST = 'https://api.foursquare.com'
# FOURSQUARE_API_PATH = '/v2/venues/search'
FOURSQUARE_API_PATH = '/v2/venues/explore'
FOURSQUARE_CONSUMER_KEY = 'WKU5S40TPL0OUM40JIY0TALMYZEN4F4VRJBF0REHVMJUUTSM'
FOURSQUARE_CONSUMER_SECRET = 'IPZLGEQGCTGRF5O1R4V23IKKLBALS0FDVAVCQMS2TWTVH5AR'

# SoundCloud
SOUNDCLOUD_CLIENT_ID = '1fc2fd9753cd0ef4560355e9e40d40da'
SOUNDCLOUD_SECRET = 'aeef7d7ad4301306b2c8900d760665e7'
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


GLOBALS_STATIC_ROOT = os.path.join(SITE_ROOT, 'apps/globals/static')


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'globals.context_processors.global_common',
 )


AUTH_PROFILE_MODULE = 'user_profiles.UserProfile'

USE_LESS = True
SITE_DOMAIN = 'localhost:8000'


### Photos
PHOTOS_MAX_SIZE = 10485760 # (10MB) max photo size, bytes
PHOTOS_FORMATS = ['jpg', 'png', 'bmp', 'gif', 'jpeg', 'jpe'] # list of imghdr-accepted formats
DOWNLOAD_DIRECTORY = '/tmp/'

### Testing
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SELENIUM_URL_ROOT = 'http://localhost.local:8000'
LIVE_SERVER_PORT = 8000
SKIP_SLOW_TESTS = True
DUMMY_THREADS = False

REAL_TIME_SEARCH_INDEX = True
USE_REDIS_QUEUE = True  # Only effective whtn REAL_TIME_SEARCH_INDEX == True

### MSN
MSN_CLIENT_ID = "00000000400C4734"
MSN_CLIENT_SECRET = "AesCLIj-RAqXzrK8QIkGrzqSpbyhwWSF"

### SSL
SSL = False

### MAIL
SEND_EMAIL = True

### IMAGEKIT
# IMAGEKIT_DEFAULT_IMAGE_CACHE_BACKEND = 'imagekit.imagecache.celery.CeleryImageCacheBackend'
IMAGEKIT_DEFAULT_IMAGE_CACHE_BACKEND = 'imagekit.imagecache.NonValidatingImageCacheBackend'


### Haystack
HAYSTACK_SOLR_URL = "http://127.0.0.1:8983/solr"
HAYSTACK_REPLICATION_SOLR = False
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr',
        'DISTANCE_AVAILABLE': True,
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}


### Facebook
FACEBOOK_APP_ID = ""
FACEBOOK_APP_SECRET = ""
FACEBOOK_APP_ACCESS_TOKEN = ""
FACEBOOK_SCOPE = "publish_stream,user_photos,email,user_birthday,user_checkins,user_activities,user_location,user_status,read_stream,offline_access"


import djcelery
djcelery.setup_loader()

USE_REDIS_QUEUE = False

# Queue
QUEUE_BACKEND = 'redisd'
QUEUE_REDIS_CONNECTION = 'localhost:6379'

### Task Queue
BROKER_HOST = "localhost"
BROKER_BACKEND = "redis"
REDIS_PORT = 6379
REDIS_HOST = "localhost"
BROKER_USER = ""
BROKER_PASSWORD = ""
BROKER_VHOST = "0"
REDIS_DB = 0
REDIS_CONNECT_RETRY = True
CELERY_SEND_EVENTS = True
CELERY_RESULT_BACKEND = 'redis'
CELERY_TASK_RESULT_EXPIRES = 10
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

SLUG_RESTRICTED_KEYWORDS = INSTALLED_APPS+ (
    'about',
    'twitter',
    'admin',
    'my_admin',
    'media',
    'static',
)


"""
### Videos
VIDEO_FORMATS = ['mp4', 'avi', 'mpg', 'wmv', 'mov']

VIDEO_SIZE = '480:-1'
VIDEO_URL = "videos/"
VIDEO_THUMBNAIL_URL = os.path.join(VIDEO_URL, 'thumbnails/')
VIDEO_MEDIA_ROOT = os.path.join(SITE_ROOT, 'S3')
VIDEO_HOST = os.path.join(SITE_DOMAIN, 'S3')
VIDEO_STREAMER = "rtmp://sgjo2itdxeldw.cloudfront.net/cfx/st"

DEFAULT_GEO_ID = 1668338
"""

## APNS
# Full path to the APN Certificate / Private Key .pem
"""
IPHONE_SANDBOX_APN_PUSH_CERT = os.path.join(SITE_ROOT, 'configs/xen/apns_keys/apns-dev2.pem')


IPHONE_APP_ID = 'com.threath'
APNS_ENV = 'sandbox'

PYAPNS_CONFIG = {
  'HOST': 'http://localhost:7077/',
  'TIMEOUT': 15,                    # OPTIONAL, host timeout in seconds
  'INITIAL': [                      # OPTIONAL, see below
    (IPHONE_APP_ID, IPHONE_SANDBOX_APN_PUSH_CERT, APNS_ENV),
  ]
}
"""

try:
    from settings_local import *
except ImportError:
    pass
