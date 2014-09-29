"""
Django settings for CrowdSourcing project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates', 'DataEntry/templates'),)
FIXTURE_DIRS = ['E:/django/contribute_vitacollections/fixtures', 'DataEntry/fixtures']

#TODO: fix to correct values on deployment
MEDIA_ROOT = 'E:/django/contribute_vitacollections/media'
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#1o30fhnkicq^whpzcw*47zh$kr3r=db+y)v_$=+21x#6swqho'

# TODO: SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    #extra modules via pip
    'south',
    'tastypie',
    #plus our local applications
    'DataEntry',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'CrowdSourcing.urls'

WSGI_APPLICATION = 'CrowdSourcing.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'contribute_vitacollections',
        'USER': 'postgres',
        'PASSWORD': 'XXXX',
        'HOST': '127.0.0.1',
        'PORT': '1111',
    }
}
#TODO: check whether to modify on migration
#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#        'URL': 'http://127.0.0.1:8983/solr/crowdsourcing'
#    },
#    'geonames': {
#        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#        'URL': 'http://127.0.0.1:8983/solr/geonames',
#        'HAYSTACK_ID_FIELD':'haystack_id',
#        'HAYSTACK_DOCUMENT_FIELD' : 'name',
#        'HAYSTACK_LIMIT_TO_REGISTERED_MODELS':'False'
#    },
#    'cangazetteer': {
#        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#        'URL': 'http://127.0.0.1:8983/solr/cangazetteer'
#    },
#    'crowdsourcing': {
#        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#        'URL': 'http://127.0.0.1:8983/solr/crowdsourcing'
#    },
#}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-ca'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#TODO: fix to correct values on deployment
LOCALE_PATHS = (
    'E:/django/common_files/locale'
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

#TODO: fix to correct values on deployment
STATIC_URL = 'http://images.ourontario.ca/static/'
SOLR_INDEX_URL = 'http://127.0.0.1:8082/solr481/'


THUMBNAIL_SIZE = 150,150
THUMBNAIL_QUALITY = 75
THUMBNAIL_EXTENSION = 't.jpg'
THUMBNAIL_RECORD_OBJECT_CATEGORY = 0

REGULAR_SIZE = 400,400
REGULAR_QUALITY = 75
REGULAR_EXTENSION = 'r.jpg'
REGULAR_RECORD_OBJECT_CATEGORY = 1

FULL_SIZE = 1600,1600
FULL_QUALITY = 75
FULL_EXTENSION = 'f.jpg'
FULL_RECORD_OBJECT_CATEGORY = 2

TEXT_RECORD_OBJECT_CATEGORY = 10

FILE_PREFIX = "Contribute"
PROJECT_MEDIA_ROOT = MEDIA_ROOT + '/project/'


OOT_PATH = 'https://data.vitatoolkit.ca/Vita40Test/'
OOTR_PATH = 'https://data.vitatoolkit.ca/Vita40Train/'
OOM_PATH = 'https://data.vitatoolkit.ca/MarineVita40/'
OOV_PATH = 'https://data.vitatoolkit.ca/Vita402/'
