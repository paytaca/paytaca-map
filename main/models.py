from django.db import models
from django.db.models import F
from django.db.models.functions import Coalesce
from django.core.validators import RegexValidator

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    short_name = models.CharField(max_length=50, unique=True, db_index=True, null=True, blank=True, validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]+$',
            message='Short name must contain only alphanumeric characters with no spaces',
            code='invalid_short_name'
        )
    ])
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class MerchantQuerySet(models.QuerySet):
    
    def with_effective_date(self):
        return self.annotate(
            effective_date=Coalesce('last_transaction_date', 'last_update')
        ).order_by('-effective_date')

class Merchant(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    watchtower_merchant_id = models.IntegerField(null=True)
    website_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    gmap_business_link = models.URLField(blank=True, null=True)
    last_transaction_date = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField(null=True, blank=True)
    test_shop = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

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
    categories = models.ManyToManyField(Category, blank=True)

    # Logo fields
    logo_size = models.CharField(max_length=10, null=True)
    logo_url = models.URLField(null=True)

    objects = MerchantQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-last_transaction_date', '-last_update']
