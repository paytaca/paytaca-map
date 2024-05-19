#First Type the command "py manage.py shell"

from main.models import Merchants, Location, Category, Vault, Logo

# Delete all objects in each model
Merchants.objects.all().delete()
Category.obejects.all().delete()
Location.objects.all().delete()
Vault.objects.all().delete()
Logo.objects.all().delete()