###################
# IMPORTS SECTION #
###################
# Django Libraries
from django.apps import apps
# Celery Libraries
from celery import shared_task
# Project Libraries
from .signals import app_ready


#################
# TASKS SECTION #
#################
# Update Articles Database - ran in the background every ~6 hours ( at usual down-times )
# Split by News Source for better efficiency

# NEWS SOURCE: ANTENA SPORT
@shared_task
def updateArticlesAS():

    # Ensure apps are ready
    if not apps.ready:

        # Use a flag to wait until the app is ready
        app_ready.connect(_run_periodic_updateAS)
    else:
        from .utils import periodicUpdateAS
        periodicUpdateAS()


def _run_periodic_updateAS(sender, **kwargs):
    from .utils import periodicUpdateAS
    periodicUpdateAS()


# NEWS SOURCE: BIHOREANUL
@shared_task
def updateArticlesBIHON():
    # Ensure apps are ready
    if not apps.ready:

        # Use a flag to wait until the app is ready
        app_ready.connect(_run_periodic_updateBIHON)
    else:
        from .utils import periodicUpdateBIHON
        periodicUpdateBIHON()


def _run_periodic_updateBIHON(sender, **kwargs):
    from .utils import periodicUpdateBIHON
    periodicUpdateBIHON()


# NEWS SOURCE: DIGI24
@shared_task
def updateArticlesDIGI24():
    # Ensure apps are ready
    if not apps.ready:

        # Use a flag to wait until the app is ready
        app_ready.connect(_run_periodic_updateDIGI24)
    else:
        from .utils import periodicUpdateDIGI24
        periodicUpdateDIGI24()


def _run_periodic_updateDIGI24(sender, **kwargs):
    from .utils import periodicUpdateDIGI24
    periodicUpdateDIGI24()


# NEWS SOURCE: PROTV
@shared_task
def updateArticlesPROTV():
    # Ensure apps are ready
    if not apps.ready:

        # Use a flag to wait until the app is ready
        app_ready.connect(_run_periodic_updatePROTV)
    else:
        from .utils import periodicUpdatePROTV
        periodicUpdatePROTV()


def _run_periodic_updatePROTV(sender, **kwargs):
    from .utils import periodicUpdatePROTV
    periodicUpdatePROTV()


# NEWS SOURCE: ZIARUL FINANCIAR
@shared_task
def updateArticlesZF():
    # Ensure apps are ready
    if not apps.ready:

        # Use a flag to wait until the app is ready
        app_ready.connect(_run_periodic_updateZF)
    else:
        from .utils import periodicUpdateZF
        periodicUpdateZF()


def _run_periodic_updateZF(sender, **kwargs):
    from .utils import periodicUpdateZF
    periodicUpdateZF()
