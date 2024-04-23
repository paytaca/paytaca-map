from django.contrib import admin
from .models import Location, Logo, Vault, Merchants, Category
# Register your models here.

admin.site.register(Merchants)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Logo)
admin.site.register(Vault)
