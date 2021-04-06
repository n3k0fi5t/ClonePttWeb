"""
Django settings for webapp project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from posix import EX_CANTCREAT, POSIX_FADV_RANDOM

product_env = os.getenv("WEBAPP_ENV", "dev") == "production"
if product_env:
    from .product_settings import *
else:
    from .dev_settings import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qcverzsmiw3%lo3zq3+1^7m#jtj@rz@ww1l#8r2^#w30qcj$0%'

# SECURITY WARNING: don't run with debug turned on in production!

# Application definition

BUILTIN_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJ_APPS = [
    'home',
    'post',
    'crawl',
]

THIRDPARTY_APPS = [
]

INSTALLED_APPS = BUILTIN_APPS + PROJ_APPS + THIRDPARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webapp.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

if DEBUG and DB_DEBUG:
    LOGGING = {
        'version' : 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console', ],
                'propagate': True,
                'level': 'DEBUG',
            }
        }
    }

# Celery settings
from kombu import Queue, Exchange

single_exchange = Exchange('reused', type='topic')
period_exchange = Exchange('period_tasks', type='direct')

CELERY_TASK_DEFAULT_QUEUE = 'web'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'app.default'
CELERY_TASK_QUEUES = (
    Queue('imme', exchange=single_exchange, routing_key='imme.#'),
    Queue('web', exchange=single_exchange, routing_key='app.#'),
    Queue('period', exchange=period_exchange, routing_key='crawl.#'),
)

CELERY_TASK_ROUTES = {
        'home.tasks.add_board': {
            'queue': 'web',
            'routing_key': 'app.add_board',
        },
        'crawl.tasks.period_crawl_task': {
            'queue': 'period',
            'routing_key': 'crawl.period',
        },
        'crawl.tasks.update_article': {
            'queue': 'imme',
            'routing_key': 'imme.update',
        },
}