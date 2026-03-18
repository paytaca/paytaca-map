from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
from django.core.cache import cache
from django.conf import settings
from .models import Merchant, Category
from .serializers import MerchantsSerializer


def get_merchants_cache_version():
    """Get the current cache version for merchants. Increments on data changes."""
    version_key = "merchants_cache_version"
    version = cache.get(version_key)
    if version is None:
        cache.set(version_key, 1, None)  # Store indefinitely
        return 1
    return version


def get_cache_key(prefix, *args, version=None):
    """Generate a cache key with optional version for cache invalidation."""
    base_key = f"{prefix}:{':'.join(str(arg) for arg in args if arg)}"
    if version:
        return f"{base_key}:v{version}"
    return base_key


class MerchantListView(APIView):
    def get(self, request):
        filter_by_id = request.query_params.get("filter_by_id")
        category_id = request.query_params.get("category_id")
        category_short_name = request.query_params.get("category")

        # Get cache version for invalidation support
        cache_version = get_merchants_cache_version()

        # Generate cache key based on query parameters and version
        cache_key = get_cache_key(
            "merchants",
            filter_by_id,
            category_id,
            category_short_name,
            version=cache_version,
        )

        # Try to get from cache first
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        merchants = (
            Merchant.objects.with_effective_date()
            .filter(test_shop=False)
            .exclude(name__regex=r"(^|\s)Test(\s|$)")
        )
        # Exclude merchants without last_transaction_date, except for Hotels/Resorts by Hiverooms category
        merchants = merchants.filter(
            models.Q(last_transaction_date__isnull=False)
            | models.Q(categories__name="Hotels / Resorts by Hiverooms")
        )
        # Exclude merchants without longitude and latitude
        merchants = merchants.filter(longitude__isnull=False, latitude__isnull=False)

        # Debug: Check if Test merchants are still there
        test_merchants = merchants.filter(name__regex=r"(^|\s)Test(\s|$)")
        if test_merchants.exists():
            print(
                f"WARNING: Found {test_merchants.count()} merchants with 'Test' in name after exclusion"
            )
            for merchant in test_merchants:
                print(f"  - {merchant.name}")

        if filter_by_id:
            merchant_ids = [int(id) for id in filter_by_id.split(",") if id.isdigit()]
            merchants = merchants.filter(id__in=merchant_ids)
        if category_id:
            merchants = merchants.filter(categories__id=category_id)
        if category_short_name:
            merchants = merchants.filter(categories__short_name=category_short_name)

        # Ensure unique merchants by ID to prevent duplicates
        merchants = merchants.distinct()

        serializer = MerchantsSerializer(merchants, many=True)
        data = serializer.data

        # Cache the result
        cache.set(cache_key, data, getattr(settings, "MERCHANTS_CACHE_TIMEOUT", 300))

        return Response(data)


class LocationListAPIView(APIView):
    def get(self, request):
        # Get cache version for invalidation support
        cache_version = get_merchants_cache_version()
        cache_key = f"locations:all:v{cache_version}"

        # Try to get from cache first
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        merchants = (
            Merchant.objects.filter(test_shop=False)
            .filter(
                models.Q(last_transaction_date__isnull=False)
                | models.Q(categories__name="Hotels / Resorts by Hiverooms")
            )
            .filter(longitude__isnull=False, latitude__isnull=False)
            .distinct()
        )

        locations = [
            {
                "id": merchant.id,
                "merchant": merchant.id,
                "landmark": merchant.landmark,
                "location": merchant.location,
                "street": merchant.street,
                "town": merchant.town,
                "city": merchant.city,
                "province": merchant.province,
                "state": merchant.state,
                "country": merchant.country,
                "longitude": merchant.longitude,
                "latitude": merchant.latitude,
            }
            for merchant in merchants
        ]

        # Cache the result
        cache.set(
            cache_key, locations, getattr(settings, "MERCHANTS_CACHE_TIMEOUT", 300)
        )

        return Response(locations)


class CategoryListAPIView(APIView):
    def get(self, request):
        # Get cache version for categories
        cache_version = cache.get("categories_cache_version")
        if cache_version is None:
            cache.set("categories_cache_version", 1, None)
            cache_version = 1
        cache_key = f"categories:all:v{cache_version}"

        # Try to get from cache first
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        categories = Category.objects.all()
        data = [
            {
                "id": category.id,
                "name": category.name,
                "short_name": category.short_name,
            }
            for category in categories
        ]

        # Cache the result with longer timeout since categories rarely change
        cache.set(cache_key, data, getattr(settings, "CATEGORIES_CACHE_TIMEOUT", 3600))

        return Response(data)


class LogoListAPIView(APIView):
    def get(self, request):
        # Get cache version for invalidation support
        cache_version = get_merchants_cache_version()
        cache_key = f"logos:all:v{cache_version}"

        # Try to get from cache first
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        merchants = (
            Merchant.objects.filter(test_shop=False)
            .filter(
                models.Q(last_transaction_date__isnull=False)
                | models.Q(categories__name="Hotels / Resorts by Hiverooms")
            )
            .filter(longitude__isnull=False, latitude__isnull=False)
            .distinct()
        )

        logos = [
            {
                "id": merchant.id,
                "merchant": merchant.id,
                "size": merchant.logo_size,
                "url": merchant.logo_url,
            }
            for merchant in merchants
            if merchant.logo_url
        ]

        # Cache the result
        cache.set(cache_key, logos, getattr(settings, "MERCHANTS_CACHE_TIMEOUT", 300))

        return Response(logos)
