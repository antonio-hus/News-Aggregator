from celery import shared_task
from django.apps import apps
from django.dispatch import receiver
from .signals import app_ready


@shared_task
def updateArticles():
    # Ensure apps are ready
    if not apps.ready:
        # Use a flag to wait until the app is ready
        app_ready.connect(_run_periodic_update)
    else:
        from .utils import periodicUpdate
        periodicUpdate()


def _run_periodic_update(sender, **kwargs):
    from .utils import periodicUpdate
    periodicUpdate()
