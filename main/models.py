from django.db import models

class Merchant(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    watchtower_merchant_id = models.IntegerField(null=True)
    website_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gmap_business_link = models.URLField(blank=True, null=True)
    last_transaction_date = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(null=True, blank=True)
    test_shop = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-last_transaction_date']

class Location(models.Model):
    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE) 
    landmark = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255, null=True)
    town = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    province = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True, db_index=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=10)
    latitude = models.DecimalField(max_digits=20, decimal_places=10)

class Category(models.Model):
    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE) 
    category = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name_plural = 'Categories'

class Vault(models.Model):
    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE) 
    address = models.CharField(max_length=255, null=True)
    token_address = models.CharField(max_length=255, null=True)

class Logo(models.Model):
    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE) 
    size = models.CharField(max_length=10, null=True)
    url = models.URLField(null=True)

