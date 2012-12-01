from dal.settings.common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dal_dev',
        'USER': 'dal',
        'PASSWORD': 'fakepass',
        'HOST': '',
        'PORT': '',
    }
}

