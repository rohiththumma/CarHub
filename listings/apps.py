# File: listings/apps.py

from django.apps import AppConfig

class ListingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listings'

    # Add this method to import your signals
    def ready(self):
        import listings.signals
