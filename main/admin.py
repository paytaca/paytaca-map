from django.contrib import admin
from .models import Merchant, Category, FeedPost
from .oembed import fetch_tiktok_thumbnail


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name", "description"]


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "city",
        "country",
        "get_categories",
        "active",
        "test_shop",
        "verified",
        "nfc_enabled",
        "last_transaction_date",
    ]
    list_filter = ["active", "test_shop", "verified", "nfc_enabled", "country", "city", "categories"]
    search_fields = ["name", "city", "country", "description"]
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "categories",
                    "description",
                    "website_url",
                    "gmap_business_link",
                    "active",
                    "test_shop",
                    "verified",
                    "nfc_enabled",
                )
            },
        ),
        (
            "Location",
            {
                "fields": (
                    "landmark",
                    "location",
                    "street",
                    "town",
                    "city",
                    "province",
                    "state",
                    "country",
                    "longitude",
                    "latitude",
                )
            },
        ),
        ("Logo", {"fields": ("logo_size", "logo_url")}),
        ("Dates", {"fields": ("last_transaction_date", "last_update")}),
    )

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    get_categories.short_description = "Categories"


@admin.register(FeedPost)
class FeedPostAdmin(admin.ModelAdmin):
    list_display = ["platform", "link", "posted_at", "active", "created_at"]
    list_filter = ["platform", "active"]
    search_fields = ["link", "description"]
    filter_horizontal = ["merchants"]
    date_hierarchy = "posted_at"
    actions = ["fetch_tiktok_thumbnails"]
    fieldsets = (
        (
            "Post",
            {
                "fields": (
                    "platform",
                    "link",
                    "image",
                    "image_url",
                    "description",
                    "posted_at",
                    "active",
                )
            },
        ),
        ("Merchants", {"fields": ("merchants",)}),
    )

    def save_model(self, request, obj, form, change):
        if obj.platform == FeedPost.Platform.TIKTOK and not obj.image and not obj.image_url:
            obj.image_url = fetch_tiktok_thumbnail(obj.link)
        super().save_model(request, obj, form, change)

    @admin.action(description="Fetch TikTok thumbnails (oEmbed)")
    def fetch_tiktok_thumbnails(self, request, queryset):
        updated = 0
        for post in queryset.filter(platform=FeedPost.Platform.TIKTOK):
            if post.image_url:
                continue
            thumbnail = fetch_tiktok_thumbnail(post.link)
            if thumbnail:
                post.image_url = thumbnail
                post.save(update_fields=["image_url"])
                updated += 1
        self.message_user(request, f"Fetched {updated} thumbnail(s).")
