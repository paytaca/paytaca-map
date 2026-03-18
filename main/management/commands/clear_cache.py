from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = "Clear all cached data for the API endpoints"

    def handle(self, *args, **options):
        try:
            # Try to clear all cache keys with a pattern
            # Database cache doesn't support keys(), so we need alternative approaches
            # Clear specific known cache keys
            keys_to_delete = [
                "categories:all",
                "locations:all",
                "logos:all",
                "merchants_cache_version",
            ]

            # For merchants, we need to clear all possible filter combinations
            # This is a limitation of database cache - we can't easily enumerate keys
            # The solution is to use cache versioning

            cache.delete_many(keys_to_delete)

            # Also try to delete any merchants:* keys if supported
            try:
                merchant_keys = cache.keys("merchants:*")
                if merchant_keys:
                    cache.delete_many(merchant_keys)
                    self.stdout.write(
                        f"Deleted {len(merchant_keys)} merchant cache keys"
                    )
            except (AttributeError, NotImplementedError):
                # Database cache doesn't support keys() - version-based cache handles this
                # Increment the version to effectively invalidate all merchant caches
                version_key = "merchants_cache_version"
                current_version = cache.get(version_key, 0)
                cache.set(version_key, current_version + 1, None)
                self.stdout.write("Incremented merchants cache version")

            self.stdout.write(self.style.SUCCESS("Successfully cleared cache"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error clearing cache: {e}"))
