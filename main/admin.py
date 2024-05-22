from django.contrib import admin
from .models import Location, Logo, Vault, Merchant, Category
# Register your models here.


class MerchantAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'gmap_business_link'
    ]

admin.site.register(Merchant, MerchantAdmin)


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Logo)
admin.site.register(Vault)
