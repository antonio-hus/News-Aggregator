###################
# IMPORTS SECTION #
###################
# Python Libraries
from __future__ import absolute_import, unicode_literals
import os
# Celery Libraries
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thedailyreport.settings')

# Create celery Application
app = Celery('thedailyreport')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure CeleryBeat Scheduled Tasks
app.conf.beat_schedule = {
    'periodic-update-AS-every-6-hours': {
        'task': 'news.tasks.updateArticlesAS',
        'schedule': crontab(minute='0', hour='*/6'),
    },
    'periodic-update-BIHON-every-6-hours': {
        'task': 'news.tasks.updateArticlesBIHON',
        'schedule': crontab(minute='0', hour='*/6'),
    },
    'periodic-update-DIGI24-every-6-hours': {
        'task': 'news.tasks.updateArticlesDIGI24',
        'schedule': crontab(minute='0', hour='*/6'),
    },
    'periodic-update-PROTV-every-6-hours': {
        'task': 'news.tasks.updateArticlesPROTV',
        'schedule': crontab(minute='0', hour='*/6'),
    },
    'periodic-update-ZF-every-6-hours': {
        'task': 'news.tasks.updateArticlesZF',
        'schedule': crontab(minute='0', hour='*/6'),
    },
}
