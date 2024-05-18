import json
from django.core.management.base import BaseCommand
from PaytacaApp.models import Location

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open('merchants.json') as f:
            data = json.load(f)
            for item in data['results']:
                Location.objects.create(
                    id=item['id'],
                    name=item['name'],
                    landmark=item['location']['landmark'],
                    location=item['location']['location'],
                    street=item['location']['street'],
                    city=item['location']['city'],
                    country=item['location']['country'],
                    longitude=item['location']['longitude'],
                    latitude=item['location']['latitude'],
                    website_url=item['website_url'],
                    category=item['category'],
                    description=item['description'],
                    gmap_business_link=item['gmap_business_link'],
                    last_transaction_date=item['last_transaction_date'],
                    receiving_pubkey=item['receiving_pubkey'],
                    receiving_address=item['receiving_address'],
                    # Add other fields here
                )
