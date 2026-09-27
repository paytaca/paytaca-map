from django.contrib import admin
from .models import Merchant, Category, FeedPost


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
    fieldsets = (
        (
            "Post",
            {
                "fields": (
                    "platform",
                    "link",
                    "description",
                    "posted_at",
                    "active",
                )
            },
        ),
        ("Merchants", {"fields": ("merchants",)}),
    )
