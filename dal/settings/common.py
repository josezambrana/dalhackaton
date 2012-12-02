# -*- coding: utf-8 -*-
import os

# ===========================================
# Settings for dal
# ===========================================

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
#    ('Your Name', 'your@mail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/La_Paz'
LANGUAGE_CODE = 'es-es'

SITE_ID = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

ROOT_URLCONF = 'dal.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dal.wsgi.application'


USE_I18N = True
USE_L10N = True
USE_TZ = True

# Paths
# -------------------------------------
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
PUBLIC_DIR = os.path.abspath(os.path.join(PROJECT_DIR, '..', '..', 'public'))
PROJECT_NAME = PROJECT_DIR.split('/')[-1]

MEDIA_ROOT = os.path.abspath(os.path.join(PUBLIC_DIR, 'media'))
MEDIA_URL = ''

STATIC_ROOT = os.path.abspath(os.path.join(PUBLIC_DIR, 'static'))
STATIC_URL = '/static/'

# Static
# -------------------------------------
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Template
# -------------------------------------
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",

    # Basic
    "common.context_processors.basic",
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Middleware
# -------------------------------------
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # third-party basic
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


# Apps
# -------------------------------------
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.markup',

    # third-party basic
    'less',
    'gunicorn',
    'debug_toolbar',
    'south',
    'taggit',

    # Dal
    'educacion',

    # zero apps # Uncomment after syncdb
    'common', 
    'users',
    'thumbnails',
    'socialauth',

)


# Logging
# -------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'verbose': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
        },  
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'project.simple': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}

# Project Config
AUTH_PROFILE_MODULE = 'users.Profile'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/usuarios/login'

# =====================================
# Third party Configuration
# =====================================

# Debug Toolbar
# -------------------------------------

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
def custom_show_toolbar(request):
    return DEBUG #request.user.is_staff and DEBUG

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'INTERCEPT_REDIRECTS': False,
}


# Common
# -------------------------------------
SITE_FROM_EMAIL = 'zeroservidor@gmail.com'
SITE_KEYWORDS = ''
SITE_DESCRIPTION = ''
