###################
# IMPORTS SECTION #
###################
# Django Libraries
from django.apps import AppConfig


######################
# APP CONFIGURATIONS #
######################
# News App Configurations
class NewsConfig(AppConfig):

    # Application Configurations
    name = 'news'

    # Database Configurations
    default_auto_field = 'django.db.models.BigAutoField'

    # Signals
    # Sends a signal when all apps are ready ( loaded )
    def ready(self):
        from .signals import app_ready
        app_ready.send(sender=self)
