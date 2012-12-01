from dal.settings.common import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

def custom_show_toolbar(request):
    return False

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'INTERCEPT_REDIRECTS': False,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dal_dev',
        'USER': 'dal',
        'PASSWORD': '0F.jz842011',
        'HOST': '',
        'PORT': '',
    }
}

