# coding: utf-8
"""
Django settings for resume project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import sys
from decouple import config
from dj_database_url import parse as db_url
from unipath import Path
BASE_DIR = Path(__file__).parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

TEMPLATE_DEBUG = DEBUG

TESTING = 'test' in sys.argv

ALLOWED_HOSTS = ['.localhost', '127.0.0.1', 'alexfalcucci.herokuapp.com', 'alexfalcucci.com', 'www.alexfalcucci.com', '*.alexfalcucci.com', '*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

PROJECT_APPS = (
    'debug_toolbar',
    'cloudinary',
    'disqus',
    'django_extensions',
    'devserver',
    'south',
    'twitter_feed',
    'resume.core',
)

INSTALLED_APPS += PROJECT_APPS

CLOUDINARY = {
    'cloud_name': 'alexfalcucci',  # config('CLOUDINARY_NAME'),
    'api_key': '566357691686394',   # config('CLOUDINARY_API_KEY'),
    'api_secret': '_WHb57oMCxw1_lzwDgf5tBKYFhY'
}

DISQUS_API_KEY = 'boKSCIOSk2XbaitNXNnf3atiNYsmqssvCEiINoXcTeYhjKt8ZBaOuEEOYxfD9AOB'
DISQUS_WEBSITE_SHORTNAME = 'alexfalcucci'

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'resume.urls'

WSGI_APPLICATION = 'resume.wsgi.application'

# data access of my account


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + BASE_DIR.child('db.sqlite3'),
        cast=db_url),
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-BR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = BASE_DIR.child('staticfiles')
STATIC_URL = '/static/'


# Cache
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

CACHE_ACTIVE = config('CACHE_ACTIVE', default=False, cast=bool)

if CACHE_ACTIVE:
    CACHES = {
        'default': {
                'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
                'BINARY': True,
                'LOCATION': config('CACHE_LOCATION'),
                'OPTIONS': {
                    'ketama': True,
                    'tcp_nodelay': True,
                },
                'TIMEOUT': config('CACHE_TIMEOUT', default=500, cast=int),
            },
    }
else:  # Assume development mode
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


# Templates
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)
TEMPLATE_STRING_IF_INVALID = 'CONTEXT_ERROR'


# Logging
def skip_on_testing(record):
    return not TESTING


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'normal': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
    },
    'filters': {
     'require_debug_true': {
         '()': 'django.utils.log.RequireDebugTrue',
         },
     'skip_on_testing': {
        '()': 'django.utils.log.CallbackFilter',
        'callback': skip_on_testing,
        },
    },
    'handlers': {
        'stderr': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'normal',
            'filters': ['skip_on_testing'],
        },
    },
    'loggers': {
        'resume': {
            'handlers': ['stderr'],
            'level': 'INFO',
        },
    },
}
