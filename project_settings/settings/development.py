from .base import *

DEBUG = True

# ALLOWED_HOSTS = ['18.216.131.139','dawat.io','www.dawat.io']

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auctiondb',
        'USER': 'postgres',
        'PASSWORD': 'admin1234',
        'HOST': "localhost",
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


#Email Backend and settings
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# static file configuration
# AWS_ACCESS_KEY_ID = 'AKIAT7WBKXHYQ7DQJ6WJ'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_STORAGE_BUCKET_NAME = 'dawat-bucket'
# AWS_S3_CUSTOM_DOMAIN = 'd3r5328bi62fu6.cloudfront.net'
# AWS_LOCATION = 'static'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#the media storage configurations
# DEFAULT_FILE_STORAGE = 'dawat.storage_backends.MediaStorage'
# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)


STATIC_URL = 'static/'
if DEBUG:
   STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'static'),
   ]
else:
   STATIC_ROOT = os.path.join(BASE_DIR,'static')

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

# settings.py
CELERY_BEAT_SCHEDULE = {
    'send-active-users-count-periodically': {
        'task': 'product.tasks.send_active_users_count_periodically',
        'schedule': 10,  # Run every 10 seconds
    },
}
