from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import User

@receiver([post_save, post_delete], sender=User)
def clear_user_cache(sender, **kwargs):
    """
    Automatically clear the Redis cache whenever a User is created, updated, or deleted.
    """
    cache_key = "cached_users"
    cache.delete(cache_key)
    print("🧹 User cache cleared due to change in User model!")
