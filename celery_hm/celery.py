import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_hm.settings')

app = Celery('celery_hm')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

app.conf.beat_schedule = {
    'pars-every-odd-hour': {
        'task': 'core.tasks.parser',
        'schedule': crontab(minute=0, hour='1-23/2')
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
