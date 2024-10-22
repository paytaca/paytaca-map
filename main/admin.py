from django.contrib import admin
from .models import Location, Logo, Merchant, Category
# Register your models here.


class MerchantAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'test_shop',
        'last_transaction_date'
    ]

admin.site.register(Merchant, MerchantAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = [
        'merchant',
        'city',
        'country'
    ]

admin.site.register(Location, LocationAdmin)


class LogoAdmin(admin.ModelAdmin):
    list_display = [
        'merchant',
        'url'
    ]

admin.site.register(Logo, LogoAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'merchant',
        'category'
    ]

admin.site.register(Category, CategoryAdmin)
