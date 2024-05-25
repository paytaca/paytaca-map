from django.contrib import admin
from .models import Location, Logo, Vault, Merchant, Category
# Register your models here.


class MerchantAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'test_shop',
        'last_transaction_date'
    ]

admin.site.register(Merchant, MerchantAdmin)


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Logo)
admin.site.register(Vault)
