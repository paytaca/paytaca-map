from django.core.management.base import BaseCommand
from main.models import Merchant, Location, Vault, Logo, Category
import dateutil.parser as parser
import time, requests
import logging

logger = logging.getLogger(__name__)


def _save_merchant(merchant_data):
    last_transaction_date_str = merchant_data['last_transaction_date']
    if last_transaction_date_str:
        last_transaction_date = parser.parse(last_transaction_date_str)
    else:
        last_transaction_date = None

    merchant = Merchant.objects.create(
        watchtower_merchant_id=merchant_data['id'],
        name=merchant_data['name'],
        website_url=merchant_data['website_url'],
        description=merchant_data['description'],
        gmap_business_link=merchant_data['gmap_business_link'],
        last_transaction_date=last_transaction_date,
        receiving_pubkey=merchant_data['receiving_pubkey'],
        receiving_address=merchant_data['receiving_address']
    )
    
    location_data = merchant_data['location']
    Location.objects.create(
        merchant=merchant,
        landmark=location_data['landmark'].strip(),
        location=location_data['location'].strip(),
        street=location_data['street'].strip(),
        town=location_data['town'].strip(),
        city=location_data['city'].strip(),
        province=location_data['province'].strip(),
        state=location_data['state'].strip(),
        country=location_data['country'].strip(),
        longitude=float(location_data['longitude']),
        latitude=float(location_data['latitude'])
    )

    if merchant_data['vault']:
        vault_data = merchant_data['vault']
        Vault.objects.create(
            merchant=merchant,
            address=vault_data['address'],
            token_address=vault_data['token_address']
        )

    logos_data = merchant_data['logos']
    for size, url in logos_data.items():
        if size == '120x120':
            # Check if a logo with size 120x120 already exists for this merchant
            existing_logo = Logo.objects.filter(merchant=merchant, size=size).first()
            if existing_logo:
                # Update the existing logo entry
                existing_logo.url = url
                existing_logo.save()
            else:
                # Create a new logo entry
                Logo.objects.create(
                    merchant=merchant,
                    size=size,
                    url=url
                )

    if merchant_data['category']:
        category_data = merchant_data['category']
        Category.objects.create_or_create(
            merchant=merchant,
            category=category_data
        )

    logger.info(f'Saved: {merchant.name}')


def _update_merchant(merchant_data):
    merchant = Merchant.objects.get(watchtower_merchant_id=merchant_data['id'])

    # Update merchant details
    last_transaction_date_str = merchant_data['last_transaction_date']
    if last_transaction_date_str:
        last_transaction_date = parser.parse(last_transaction_date_str)
    else:
        last_transaction_date = None
    Merchant.objects.filter(watchtower_merchant_id=merchant_data['id']).update(
        watchtower_merchant_id=merchant_data['id'],
        name=merchant_data['name'],
        website_url=merchant_data['website_url'],
        description=merchant_data['description'],
        gmap_business_link=merchant_data['gmap_business_link'],
        last_transaction_date=last_transaction_date,
        receiving_pubkey=merchant_data['receiving_pubkey'],
        receiving_address=merchant_data['receiving_address']
    )

    # Update location
    location_data = merchant_data['location']
    if location_data:
        Location.objects.update_or_create(
            merchant=merchant,
            landmark=location_data['landmark'].strip(),
            location=location_data['location'].strip(),
            street=location_data['street'].strip(),
            town=location_data['town'].strip(),
            city=location_data['city'].strip(),
            province=location_data['province'].strip(),
            state=location_data['state'].strip(),
            country=location_data['country'].strip(),
            longitude=float(location_data['longitude']),
            latitude=float(location_data['latitude'])
        )

    # Update vault
    if merchant_data['vault']:
        vault_data = merchant_data['vault']
        Vault.objects.update_or_create(
            merchant=merchant,
            address=vault_data['address'],
            token_address=vault_data['token_address']
        )

    # Update logo
    logos_data = merchant_data['logos']
    for size, url in logos_data.items():
        if size == '120x120':
            # Check if a logo with size 120x120 already exists for this merchant
            existing_logo = Logo.objects.filter(merchant=merchant, size=size).first()
            if existing_logo:
                # Update the existing logo entry
                existing_logo.url = url
                existing_logo.save()
            else:
                # Create a new logo entry
                Logo.objects.update_or_create(
                    merchant=merchant,
                    size=size,
                    url=url
                )
    
    # Update category
    if merchant_data['category']:
        category_data = merchant_data['category']
        Category.objects.update_or_create(
            merchant=merchant,
            category=category_data
        )

    logger.info(f'Updated: {merchant.name}')


def _fetch_merchants():
    source_url = 'https://watchtower.cash/api/paytacapos/merchants/?active=true&verified=true&has_pagination=false'
    resp = requests.get(source_url)
    if resp.status_code == 200:
        merchants = resp.json()
        for merchant_data in merchants:

            merchant_check = Merchant.objects.filter(watchtower_merchant_id=merchant_data['id'])
            if merchant_check.exists():
                proceed_update = False
                merchant = merchant_check.last()
                if merchant_data['last_update']:
                    if merchant_data['last_update']:
                        if merchant.last_update:
                            _last_update = parser.parse(merchant_data['last_update'])
                            if merchant.last_update < _last_update:
                                proceed_update = True
                        else:
                            proceed_update = True
                    else:
                        proceed_update = True
                if proceed_update:
                    _update_merchant(merchant_data)
            else:
                location_data = merchant_data['location']
                if location_data['longitude']:
                    _save_merchant(merchant_data)


class Command(BaseCommand):
    help = 'Saves or updates merchants fetched from Watchtower.cash'

    def handle(self, *args, **kwargs):
        # Update merchants every 60 seconds
        while True:
            time.sleep(60)
            logger.info('Fetching merchants...')
            _fetch_merchants()
