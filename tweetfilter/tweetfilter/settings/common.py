# Django settings for tweetfilter project.
import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

TEMP_DIR = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]

PROJECT_DIR, SITE_ROOT = os.path.split(TEMP_DIR)

VAR_ROOT = os.path.join(os.path.split(PROJECT_DIR)[0], 'var')
if not os.path.exists(VAR_ROOT):
    os.mkdir(VAR_ROOT)

LOGGING_ROOT = os.path.join(os.path.split(PROJECT_DIR)[0], 'server_logs', 'dev')
if not os.path.exists(LOGGING_ROOT):
    os.mkdir(LOGGING_ROOT)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VAR_ROOT, 'twitter.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['192.168.0.103']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

#=====================================================================
# Project URL and media settings
#=====================================================================
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(VAR_ROOT, 'static')
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'wa%lk=$k#!-td3clxtb10+m)ul%4@gl5y8-7_^m-w92p1f4s%p'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'tweetfilter.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tweetfilter.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project modules
    'apps.filtering',
    'apps.twitter',
    'apps.accounts',
    'apps.control',
    'apps.scheduling',
    'apps.hashtags',
    'apps.notifications',

    # Third party modules
    'crispy_forms',
    'registration',
    'djcelery',
    'south',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s]: %(message)s'
        },
        'channel': {
            'format': '%(asctime)s [%(screen_name)s] [%(levelname)s]: %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'app.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'channels': {
            'level': 'DEBUG',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'twitter-all.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'channel',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'filters': ['require_debug_true'],
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'streaming': {
            'level': 'DEBUG',
            'class': 'cloghandler.ConcurrentRotatingFileHandler',
            'filename': os.path.join(LOGGING_ROOT, 'streaming.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'twitter': {
            'handlers': ['channels', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'app': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'streaming': {
            'handlers': ['streaming'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

#==============================================================================
# Twitter settings
#==============================================================================

TWITTER_APP_KEY = ''
TWITTER_APP_SECRET = ''


#==============================================================================
# Celery
#==============================================================================

import djcelery
djcelery.setup_loader()

BROKER_URL = 'amqp://guest:guest@localhost:5672/'
BROKER_POOL_LIMIT = 500
CELERY_RESULT_BACKEND = "amqp"
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
#CELERYD_CONCURRENCY = 4
CELERY_TIMEZONE = 'America/Caracas'
CELERY_IMPORTS = ('apps.filtering.tasks',
                  'apps.scheduling.tasks',
                  'apps.notifications.tasks')

CELERYD_PREFETCH_MULTIPLIER = 100
CELERY_ACKS_LATE = True
CELERY_IGNORE_RESULT = True


#==============================================================================
# Cache
#==============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = ""

# Crispy form configuration
CRISPY_TEMPLATE_PACK = 'bootstrap'

# Email configuration
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'AKIAI5JS2F2RLK4S5G7Q'
AWS_SECRET_ACCESS_KEY = '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'

EMAIL_FROM = "traffic.testing24@gmail.com"
