###################
# IMPORTS SECTION #
###################
# Django Libraries
from django.apps import apps
from django.dispatch import Signal


######################
# SIGNAL DEFINITIONS #
######################
# This signal is triggered when all apps are ready
app_ready = Signal()
