###################
# IMPORTS SECTION #
###################
# Python Libraries
import os
# Django Libraries
from django.core.wsgi import get_wsgi_application


##############
# WSGI LOGIC #
##############

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thedailyreport.settings')
application = get_wsgi_application()
app = application
