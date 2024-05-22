#First Type the command "py manage.py shell"

from main.models import Merchant, Location, Category, Vault, Logo

# Delete all objects in each model
Merchant.objects.all().delete()
Category.obejects.all().delete()
Location.objects.all().delete()
Vault.objects.all().delete()
Logo.objects.all().delete()