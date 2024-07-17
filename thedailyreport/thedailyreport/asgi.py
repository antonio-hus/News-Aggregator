###################
# IMPORTS SECTION #
###################
# Python Libraries
import os
# Django Libraries
from django.core.asgi import get_asgi_application

##############
# ASGI LOGIC #
##############

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thedailyreport.settings')
application = get_asgi_application()
