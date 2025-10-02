import os
from celery import Celery
from celery.schedules import schedule
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Donution.settings')

app = Celery('Donution')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


CELERY_BEAT_SCHEDULE = {
    'change-collection-status': {
        'task': 'api.tasks.old_collection_task',
        'schedule': schedule(run_every=10),
    },
}
