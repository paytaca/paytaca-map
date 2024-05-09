from django.db import models

class Merchants(models.Model): 
    name = models.CharField(max_length=255, db_index=True)
    website_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gmap_business_link = models.URLField(blank=True, null=True)
    last_transaction_date = models.DateTimeField(blank=True, null=True)
    receiving_pubkey = models.CharField(max_length=255, blank=True, null=True)
    receiving_address = models.CharField(max_length=255, blank=True, null=True)

class Location(models.Model):
    merchant = models.OneToOneField(Merchants, on_delete=models.CASCADE) 
    landmark = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True, db_index=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=10)
    latitude = models.DecimalField(max_digits=20, decimal_places=10)

class Category(models.Model):
    merchant = models.OneToOneField(Merchants, on_delete=models.CASCADE) 
    category = models.CharField(max_length=255, blank=True, null=True, db_index=True)

class Vault(models.Model):
    merchant = models.OneToOneField(Merchants, on_delete=models.CASCADE) 
    address = models.CharField(max_length=255, null=True)
    token_address = models.CharField(max_length=255, null=True)

class Logo(models.Model):
    merchant = models.OneToOneField(Merchants, on_delete=models.CASCADE) 
    size = models.CharField(max_length=10, null=True)
    url = models.URLField(null=True)

