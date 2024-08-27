import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project247livesports.settings')

app = Celery('project247livesports')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a CELERY_ prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True

# Add the beat schedule for fetching fixtures every 30 seconds
app.conf.beat_schedule = {
    'fetch-todays-yesterday-tomorrow-fixtures-every-30-seconds': {
        'task': 'soccer.tasks.fetch_fixtures_for_dates',
        'schedule': 30.0,  # Run every 30 seconds
    },
}

app.conf.timezone = 'UTC'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
