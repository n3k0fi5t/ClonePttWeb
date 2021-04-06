import os
from django.utils import timezone

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
broker = os.getenv("BROKER_DSN", 'pyamqp://guest:guest@rabbitmq/')

app = Celery('webapp', broker=broker, include=['crawl.tasks'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.now = timezone.now

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()