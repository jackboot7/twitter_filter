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

#==============================================================================
# Twitter settings
#==============================================================================

TWITTER_APP_KEY = '50MA0itOv5os7GYVFG6cKA'
TWITTER_APP_SECRET = 'MRDXuA2IWgHZt08YVFHva3gxj6SxZevLnyrH4I0Q'