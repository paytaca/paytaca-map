from django.db import models
from django.db.models import F
from django.db.models.functions import Coalesce
from django.core.validators import RegexValidator
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    short_name = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z0-9]+$",
                message="Short name must contain only alphanumeric characters with no spaces",
                code="invalid_short_name",
            )
        ],
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]


class MerchantQuerySet(models.QuerySet):
    def with_effective_date(self):
        return self.annotate(
            effective_date=Coalesce("last_transaction_date", "last_update")
        ).order_by("-effective_date")


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
    nfc_enabled = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

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
    logo_size = models.CharField(blank=True, max_length=10, null=True)
    logo_url = models.URLField(blank=True, null=True)

    objects = MerchantQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-last_transaction_date", "-last_update"]


class FeedPost(models.Model):
    class Platform(models.TextChoices):
        FACEBOOK = "facebook", "Facebook"
        TIKTOK = "tiktok", "TikTok"
        INSTAGRAM = "instagram", "Instagram"
        X = "x", "X"

    platform = models.CharField(
        max_length=20, choices=Platform.choices, db_index=True
    )
    link = models.URLField()
    image = models.ImageField(
        upload_to="feed/", blank=True, null=True,
        help_text="Upload a preview image. Takes precedence over the remote thumbnail URL.",
    )
    image_url = models.URLField(
        max_length=500, blank=True, null=True,
        help_text="Remote preview image URL. Left blank, TikTok posts are auto-filled via oEmbed.",
    )
    description = models.TextField(blank=True, null=True)
    merchants = models.ManyToManyField(
        Merchant, blank=True, related_name="feed_posts"
    )
    posted_at = models.DateTimeField(default=timezone.now, null=True, blank=True, db_index=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_platform_display()}: {self.link}"

    class Meta:
        ordering = ["-posted_at", "-created_at"]
