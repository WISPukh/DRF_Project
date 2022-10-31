import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF_Project.settings')

app = Celery('shop')

app.conf.broker_url = 'redis://redis_shop:6379/0'
app.conf.result_backend = 'redis://redis_shop:6379/0'
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
