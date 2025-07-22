# File: car_platform/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Your admin panel URL
    path('admin/', admin.site.urls),
    
    # This includes all the URLs from your 'listings' app (homepage, login, etc.)
    path('', include('listings.urls')), 
]

# This is your existing code to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
