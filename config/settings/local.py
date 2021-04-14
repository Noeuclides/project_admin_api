from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    '0.0.0.0',
    'localhost',
]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if not CONTAINER_RUNNING:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'slabcode_db',
            'USER': 'slabcode_user',
            'PASSWORD': 'slabcode_pass',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': env.db()
    }

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025