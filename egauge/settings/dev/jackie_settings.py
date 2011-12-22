from egauge.settings.common.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jackie Kazil', 'jacqueline.kazil@gmail.com'),
)

MANAGERS = ADMINS

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.contrib.gis.db.backends.postgis',
#        'NAME': 'egauge',
#        'USER': 'egauge',
#        'PASSWORD': 'egauge',
#        'HOST': 'localhost',
#        'PORT': '5432',
#    }
#}

ENV_DIR = '/Users/jakopanda/.virtualenvs/electiongauge/'
CODE_DIR = '/Users/jakopanda/Projects/code/electiongauge/egauge'

TEMPLATE_DIRS = (
    CODE_DIR,
    ENV_DIR + 'lib/python2.6/site-packages/django/contrib/admin/templates',
    ENV_DIR + 'lib/python2.6/site-packages/debug_toolbar/templates',
)

STATIC_ROOT = '/Users/jakopanda/Projects/code/electiongauge_static'
STATIC_URL = '/static'
STATICFILES_DIRS = (
    CODE_DIR + "/static",
)

INSTALLED_APPS = (
    'django.contrib.gis',
    'django.contrib.staticfiles',
    #'egauge.apps.core',
    'django_extensions',
    'debug_toolbar',
) + INSTALLED_APPS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

ROOT_URLCONF = 'egauge.settings.dev.jackie_urls'
INTERNAL_IPS = ('127.0.0.1',)
