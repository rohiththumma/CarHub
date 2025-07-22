# File: listings/signals.py

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# This function will run every time a new User object is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# This function will run every time a User object is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Ensure the user has a profile before trying to save it
    if hasattr(instance, 'profile'):
        instance.profile.save()
