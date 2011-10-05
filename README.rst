IRC Logs
========

Parses ZNC logs and puts them into a DB.

Hacking
-------

Create an ``irclogs/settings.py`` file with the following content::

    from default_settings import *

    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(HERE, 'logs.sqlite'),
        },
    }

    LOGS_DIR = '/path/to/znc/logs'

    DIRECTORIES = (
        ('', 'django-admin.py test irc --settings=irclogs.test_settings'),
    )

    SECRET_KEY = 'something'

Then::

    mkvirtualenv irclogs
    add2virtualenv .
    pip install -r requirements.txt -r requirements-dev.txt
    gem install bundle
    bundle install
    foreman start

To import your logs::

    django-admin.py parse_logs --settings=irclogs.settings
