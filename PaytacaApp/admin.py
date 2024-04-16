from django.contrib import admin
from .models import Location
from .models import Logo
from .models import Vault
# Register your models here.

admin.site.register(Location)
admin.site.register(Logo)
admin.site.register(Vault)
