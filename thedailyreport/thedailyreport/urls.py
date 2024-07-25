###################
# IMPORTS SECTION #
###################
# Django Libraries
from django.conf.urls.static import static
from . import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


################
# URL PATTERNS #
################

urlpatterns = [

    # Admin Website
    path('admin/', admin.site.urls),

    # Backend  - Django - ( API Endpoints )
    path('api/', include('news.urls')),

    # Frontend - React
    path('', TemplateView.as_view(template_name='index.html')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
