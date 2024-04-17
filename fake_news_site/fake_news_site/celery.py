import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fake_news_site.settings')

app = Celery('fake_news_site')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'send_weekly_digest': {
        'task': 'fake_news_app.tasks.send_weekly_digest',
        'schedule': crontab(day_of_week='mon', hour=8),  # Runs every Monday at 8AM
    },
}

app.autodiscover_tasks()