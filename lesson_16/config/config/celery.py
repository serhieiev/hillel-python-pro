import os
from celery import Celery
from creditcards.tasks.freeze_expired_cards import freeze_expired_cards


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

celery_app = Celery("config")

celery_app.config_from_object("django.conf:settings", namespace="CELERY")

celery_app.autodiscover_tasks(["creditcards.tasks"])
