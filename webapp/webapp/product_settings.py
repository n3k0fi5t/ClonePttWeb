import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DB_DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.getenv("POSTGRES_HOST"),
        'PORT': os.getenv("POSTGRES_PORT", "5432"),
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD")
    }
}

ALLOWED_HOSTS = ["*"]

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
        'crawl.tasks.batch_update': {
            'queue': 'period',
            'routing_key': 'crawl.update',
        },
        'crawl.tasks.update_article': {
            'queue': 'imme',
            'routing_key': 'imme.update',
        },
}

# Search engine
SEARCH_CONFIG = 'chinese'