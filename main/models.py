from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class Merchant(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    watchtower_merchant_id = models.IntegerField(null=True)
    website_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gmap_business_link = models.URLField(blank=True, null=True)
    last_transaction_date = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(null=True, blank=True)
    test_shop = models.BooleanField(default=False)

    # Location fields
    landmark = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    town = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, db_index=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=10, null=True)

    # Category field
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    # Logo fields
    logo_size = models.CharField(max_length=10, null=True)
    logo_url = models.URLField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-last_transaction_date']

