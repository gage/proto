from settings import INSTALLED_APPS

DEBUG = True

INSTALLED_APPS += ('devserver', 'django_concurrent_test_server',)

MEDIA_URL = 'http://localhost:8000/media/'

SITE_ID = '4fd55c4613e7d961b700000c'
