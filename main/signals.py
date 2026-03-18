from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.cache import cache
from .models import Merchant, Category


def clear_merchants_cache():
    """Clear all merchant-related cache by incrementing the version."""
    version_key = "merchants_cache_version"
    current_version = cache.get(version_key, 0)
    cache.set(version_key, current_version + 1, None)  # Store indefinitely


def clear_categories_cache():
    """Clear categories cache by incrementing the version."""
    version_key = "categories_cache_version"
    current_version = cache.get(version_key, 0)
    cache.set(version_key, current_version + 1, None)  # Store indefinitely


@receiver(post_save, sender=Merchant)
@receiver(post_delete, sender=Merchant)
def merchant_cache_invalidator(sender, **kwargs):
    """Invalidate merchant cache when a merchant is saved or deleted."""
    clear_merchants_cache()


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def category_cache_invalidator(sender, **kwargs):
    """Invalidate category cache when a category is saved or deleted."""
    clear_categories_cache()
    # Categories are linked to merchants via M2M, so also clear merchants cache
    clear_merchants_cache()


@receiver(m2m_changed, sender=Merchant.categories.through)
def merchant_categories_changed(sender, **kwargs):
    """Invalidate merchant cache when merchant categories change."""
    clear_merchants_cache()
