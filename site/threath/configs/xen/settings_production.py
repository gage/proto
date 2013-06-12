DEBUG = False

SITE_ID = "518c9730ae4ea472c44dd4b9"

DEFAULT_FILE_STORAGE = 's3sync.storage.S3PendingStorage'

AWS_ACCESS_KEY_ID = 'AKIAIIR2TKOBEZ33OGHA'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_UPLOADS = 'media.socialites'
BUCKET_UPLOADS_URL = 'http://media.socialites.s3.amazonaws.com/media/'

FACEBOOK_APP_ID = "487885584610206"
FACEBOOK_APP_SECRET = "09c98b1b19f831f58dbfe566246687b6"

VIDEO_HOST = "videos.sharecity.com.s3.amazonaws.com"

PRODUCTION = True

CACHES = {
    'default' : {
        'BACKEND' : 'mongo_cache.backend.MongoDBCache',
        'LOCATION': 'socialites_cache',
        'OPTIONS': {
            'DATABASE': 'gulu',
            'HOST': '10.0.0.81',
            'PORT': 27017,
        }
    }
}