from django.apps import apps
from django.dispatch import Signal


# This signal is triggered when all apps are ready
app_ready = Signal()
