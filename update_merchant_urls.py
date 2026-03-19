# Django shell script to update merchant website URLs
# Can be run standalone with: python update_merchant_urls.py
# Or pasted into: python manage.py shell

import os
import sys

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paytaca_map.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

django.setup()

from main.models import Merchant

# Map of merchant IDs to website URLs
merchant_urls = {
    263: "https://book.hiverooms.com/booking-page.php?id=8-newtown-boulevard-by-hiverooms",
    266: "https://book.hiverooms.com/booking-page.php?id=ariella-mangrove-eco-resort-by-hiverooms",
    267: "https://book.hiverooms.com/booking-page.php?id=badian-island-wellness-resort",
    268: "https://book.hiverooms.com/booking-page.php?id=bluewaves-basdaku",
    269: "https://book.hiverooms.com/booking-page.php?id=bluewaves-hostel-villa-panagsama",
    270: "https://book.hiverooms.com/booking-page.php?id=casay-beach-house-by-hiverooms",
    271: "https://book.hiverooms.com/booking-page.php?id=ceda-guesthouse-by-hiverooms",
    272: "https://book.hiverooms.com/booking-page.php?id=fandc-guest-house",
    273: "https://book.hiverooms.com/booking-page.php?id=fazenda-de-faburada-ecofarm-and-mountain-resort-by-hiverooms",
    274: "https://book.hiverooms.com/booking-page.php?id=fins-pacific-coral-bay",
    275: "https://book.hiverooms.com/booking-page.php?id=hagdan-reef-dive-spot",
    276: "https://book.hiverooms.com/booking-page.php?id=jvr-island-in-the-sky-resort-by-hiverooms",
    277: "https://book.hiverooms.com/booking-page.php?id=kalaparan-farm-house-by-hiverooms",
    279: "https://book.hiverooms.com/booking-page.php?id=mca-suites-by-hiverooms",
    283: "https://book.hiverooms.com/booking-page.php?id=mandala-beach-cebu",
    284: "https://book.hiverooms.com/booking-page.php?id=bogo-northomes-pensione",
    286: "https://book.hiverooms.com/booking-page.php?id=one-manchester-place-by-hiverooms",
    287: "https://book.hiverooms.com/booking-page.php?id=one-pacific-residences-by-hiverooms",
    288: "https://book.hiverooms.com/booking-page.php?id=rajah-park-hotel-by-hiverooms",
    289: "https://book.hiverooms.com/booking-page.php?id=rockwalled-adventure-resort-by-hiverooms",
    290: "https://book.hiverooms.com/booking-page.php?id=serenity-farm-and-resort",
    295: "https://book.hiverooms.com/booking-page.php?id=sonrisa-golden-meadows",
    296: "https://book.hiverooms.com/booking-page.php?id=sonrisa-resort-de-playa-by-hiverooms",
    297: "https://book.hiverooms.com/booking-page.php?id=tambuli-seaside-resort-and-spa",
    300: "https://book.hiverooms.com/booking-page.php?id=ipark-hotel-by-hiverooms",
    378: "https://book.hiverooms.com/booking-page.php?id=upperhouse-hotel-formerly-pacifico-boutique-by-hiverooms",
    379: "https://book.hiverooms.com/booking-page.php?id=serenity-home-7",
    380: "https://book.hiverooms.com/booking-page.php?id=serenity-home-9",
    381: "https://book.hiverooms.com/booking-page.php?id=serenity-home-11",
    382: "https://book.hiverooms.com/booking-page.php?id=casa-de-vacacion-in-orani-bataan",
}

# Update merchants
from django.db import transaction

updated = []
not_found = []

with transaction.atomic():
    for merchant_id, url in merchant_urls.items():
        try:
            # Replace 'Merchant' with your actual model name
            merchant = Merchant.objects.get(id=merchant_id)
            merchant.website_url = url
            merchant.save(update_fields=["website_url"])
            updated.append(merchant_id)
            print(f"Updated ID {merchant_id}: {merchant.name}")
        except Merchant.DoesNotExist:
            not_found.append(merchant_id)
            print(f"Not found: ID {merchant_id}")

print(f"\n=== Summary ===")
print(f"Updated: {len(updated)} merchants")
print(f"Not found: {len(not_found)} merchants")

# These merchants were not found in the API:
# 265 Almond Suites
# 280 Maayo Argao
# 281 Maayo Hotel
# 282 Maayo San Remigio
# 291 Solea Coast Resort
# 292 Solea Mactan Resort
# 293 Solea Palm Resort
# 294 Solea Seaview Resort
# 298 The Beach Park Hadsan
# 299 Torre de Alcoy
