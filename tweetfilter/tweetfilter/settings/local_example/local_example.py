import os
from common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMIN_MEDIA_PREFIX = '/static/admin/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VAR_ROOT, 'dev.db'),
    },
}

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.admindocs',
)

#=============================================
# Twitter Settings.
#=============================================

TWITTER_APP_KEY = ''
TWITTER_APP_SECRET = ''
