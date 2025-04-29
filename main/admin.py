from django.contrib import admin
from .models import Merchant, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'city',
        'country',
        'get_categories',
        'test_shop',
        'verified',
        'last_transaction_date'
    ]
    list_filter = [
        'test_shop',
        'verified',
        'country',
        'city',
        'categories'
    ]
    search_fields = [
        'name',
        'city',
        'country',
        'description'
    ]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'categories', 'description', 'website_url', 'gmap_business_link', 'test_shop', 'verified')
        }),
        ('Location', {
            'fields': (
                'landmark', 'location', 'street', 'town', 'city',
                'province', 'state', 'country', 'longitude', 'latitude'
            )
        }),
        ('Logo', {
            'fields': ('logo_size', 'logo_url')
        }),
        ('Dates', {
            'fields': ('last_transaction_date', 'last_update')
        }),
    )

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'
