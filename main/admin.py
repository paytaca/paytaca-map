from django.contrib import admin
from .models import Merchant

class MerchantAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'city',
        'country',
        'test_shop',
        'last_transaction_date'
    ]
    list_filter = [
        'test_shop',
        'category',
        'country',
        'city'
    ]
    search_fields = [
        'name',
        'category',
        'city',
        'country',
        'description'
    ]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'website_url', 'gmap_business_link', 'test_shop')
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

admin.site.register(Merchant, MerchantAdmin)
