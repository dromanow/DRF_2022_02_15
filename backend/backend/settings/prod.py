from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'library_1',
        'USER': 'denis',
        'PASSWORD': 'qwerty',
        'HOST': 'db',
        'PORT': '5432'
    }
}
