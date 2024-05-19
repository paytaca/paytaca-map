from django.core.management.base import BaseCommand
from main.models import Merchants, Location, Vault, Logo, Category
import json
from django.utils.dateparse import parse_datetime
import datetime
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Imports locations data from merchants.json'

    def handle(self, *args, **kwargs):
        filename = 'merchants.json'
        with open(filename, 'r') as file:
            data = json.load(file)
            merchants_data = data['results']

            for merchant_data in merchants_data:
                # Parse last_transaction_date
                last_transaction_date_str = merchant_data['last_transaction_date']
                if last_transaction_date_str:
                    last_transaction_date = datetime.datetime.strptime(last_transaction_date_str, '%Y-%m-%d %H:%M:%S.%f%z')
                else:
                    last_transaction_date = None

                merchant = Merchants.objects.create(
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
                    landmark=location_data['landmark'],
                    location=location_data['location'],
                    street=location_data['street'],
                    city=location_data['city'],
                    country=location_data['country'],
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
                    Category.objects.create(
                        merchant=merchant,
                        category=category_data
                    )

        self.stdout.write(self.style.SUCCESS('Successfully imported locations data.'))

