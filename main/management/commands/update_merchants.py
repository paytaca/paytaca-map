from django.core.management.base import BaseCommand
from main.models import Merchant
import dateutil.parser as parser
from django.utils import timezone
import time, requests
import logging
import pytz


logger = logging.getLogger(__name__)


def parse_last_transaction_date(datetime_string):
    if datetime_string:
        last_transaction_date_obj = parser.parse(datetime_string)
        last_transaction_date = last_transaction_date_obj.astimezone(pytz.UTC)
    else:
        last_transaction_date = None
    return last_transaction_date


def _save_merchant(merchant_data):
    logger.info(merchant_data)

    last_transaction_date_str = merchant_data['last_transaction_date']
    last_transaction_date = parse_last_transaction_date(last_transaction_date_str)

    location_data = merchant_data['location']
    logos_data = merchant_data['logos']
    logo_120x120 = logos_data.get('120x120') if logos_data else None

    merchant = Merchant.objects.create(
        watchtower_merchant_id=merchant_data['id'],
        name=merchant_data['name'],
        website_url=merchant_data['website_url'],
        description=merchant_data['description'],
        gmap_business_link=merchant_data['gmap_business_link'],
        last_transaction_date=last_transaction_date,
        last_update=timezone.now(),
        verified=merchant_data.get('verified', False),
        # Location fields
        landmark=location_data['landmark'],
        street=location_data['street'],
        town=location_data['town'],
        city=location_data['city'],
        province=location_data['province'],
        state=location_data['state'],
        country=location_data['country'],
        longitude=float(location_data['longitude']) if location_data['longitude'] is not None else None,
        latitude=float(location_data['latitude']) if location_data['latitude'] is not None else None,
        # Logo fields
        logo_size='120x120' if logo_120x120 else None,
        logo_url=logo_120x120
    )

    logger.info(f'Saved: {merchant.name}')


def _update_merchant(merchant_data):
    logger.info(merchant_data)
    merchant = Merchant.objects.get(watchtower_merchant_id=merchant_data['id'])

    # Update location
    location_data = merchant_data['location']
    if location_data:
        merchant.landmark = location_data['landmark']
        merchant.street = location_data['street']
        merchant.town = location_data['town']
        merchant.city = location_data['city']
        merchant.province = location_data['province']
        merchant.state = location_data['state']
        merchant.country = location_data['country']
        merchant.longitude = float(location_data['longitude']) if location_data['longitude'] is not None else None
        merchant.latitude = float(location_data['latitude']) if location_data['latitude'] is not None else None

    # Update logo
    logos_data = merchant_data['logos']
    logo_120x120 = logos_data.get('120x120') if logos_data else None
    if logo_120x120:
        merchant.logo_size = '120x120'
        merchant.logo_url = logo_120x120

    # Update merchant details
    last_transaction_date_str = merchant_data['last_transaction_date']
    last_transaction_date = parse_last_transaction_date(last_transaction_date_str)

    merchant.name = merchant_data['name']
    merchant.website_url = merchant_data['website_url']
    merchant.description = merchant_data['description']
    merchant.gmap_business_link = merchant_data['gmap_business_link']
    merchant.last_transaction_date = last_transaction_date
    merchant.last_update = timezone.now()
    merchant.save()

    logger.info(f'Updated: {merchant.name}')


def _fetch_merchants(check_last_update=True):
    source_url = 'https://watchtower.cash/api/paytacapos/merchants/?active=true&has_pagination=false'
    resp = requests.get(source_url)
    if resp.status_code == 200:
        merchants = resp.json()
        for merchant_data in merchants:
            merchant_check = Merchant.objects.filter(watchtower_merchant_id=merchant_data['id'])
            if merchant_check.exists():
                merchant = merchant_check.last()
                proceed_update = False
                if check_last_update:
                    if 'last_update' in merchant_data.keys():
                        if merchant_data['last_update']:
                            if merchant.last_update:
                                _last_update = parser.parse(merchant_data['last_update'])
                                if merchant.last_update < _last_update:
                                    proceed_update = True
                            else:
                                proceed_update = True
                        else:
                            proceed_update = True
                else:
                    proceed_update = True

                last_transaction_date_str = merchant_data['last_transaction_date']
                last_transaction_date = parse_last_transaction_date(last_transaction_date_str)
                if last_transaction_date:
                    last_transaction_date = parser.parse(last_transaction_date_str)
                    if merchant.last_transaction_date < last_transaction_date:
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
