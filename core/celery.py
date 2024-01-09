# core/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

celery_app = Celery('core')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover and register tasks in your apps
celery_app.autodiscover_tasks()

# Add a periodic task to print "Hello" every 10 seconds
celery_app.conf.beat_schedule = {
    'print-hello': {
        'task': 'portal.tasks.print_hello',
        'schedule': 10,  # 10 seconds
    },
}
