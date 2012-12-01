from dal.settings.common import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': 'dal_prod',
        'USER': 'dal',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
