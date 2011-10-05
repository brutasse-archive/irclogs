import os
HERE = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ADMINS

TIME_ZONE = 'Europe/Paris'

LANGUAGE_CODE = 'en-us'
SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(HERE, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(HERE, 'static')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'staticfiles.finders.FileSystemFinder',
    'staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'irclogs.urls'

TEMPLATE_DIRS = (
    os.path.join(HERE, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'staticfiles',
    'django.contrib.admin',

    'irclogs.irc',
)

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
