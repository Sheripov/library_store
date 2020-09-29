import os

from library.settings.base import *

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir
)

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'library_db',
        'USER': 'postgres',
        'PASSWORD': '1',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# for run server
# python manage.py runserver --settings library.settings.pycharm
