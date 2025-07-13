from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set default Django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'validatronn_backend.settings')

app = Celery('validatronn_backend')

# load config from Django settings, using namespace 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto-discover tasks from all installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
