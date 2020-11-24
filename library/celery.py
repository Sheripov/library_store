import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')

app = Celery('library')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-spam-every-day-of-week': {
        'task': 'books.tasks.send_beat_email',
        'schedule': crontab(minute=0, hour=0, day_of_week='sunday'),
    },
    'parsing_site': {
        'task': 'books.tasks.add_books_from_site',
        'schedule': crontab(minute=0, hour=0, day_of_week='sunday'),
    }
}
