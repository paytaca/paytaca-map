import json
from django.core.management.base import BaseCommand
from PaytacaApp.models import Location, Vault, Logo

class Command(BaseCommand):
    help = 'Import locations data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        with open(json_file, 'r') as f:
            data = json.load(f)
            results = data.get('results', [])
            
            for result in results:
                location_data = result.get('location', {})
                location = Location.objects.create(
                    name=result.get('name'),
                    landmark=location_data.get('landmark'),
                    location=location_data.get('location'),
                    street=location_data.get('street'),
                    city=location_data.get('city'),
                    country=location_data.get('country'),
                    longitude=location_data.get('longitude'),
                    latitude=location_data.get('latitude'),
                    website_url=result.get('website_url'),
                    category=result.get('category'),
                    description=result.get('description'),
                    gmap_business_link=result.get('gmap_business_link'),
                    last_transaction_date=result.get('last_transaction_date'),
                    receiving_pubkey=result.get('receiving_pubkey'),
                    receiving_address=result.get('receiving_address')
                )
                
                # Create Vault instance if available
                vault_data = result.get('vault')
                if vault_data:
                    Vault.objects.create(
                        location=location,
                        address=vault_data.get('address'),
                        token_address=vault_data.get('token_address')
                    )
                
                # Create Logo instances if available
                logos_data = result.get('logos', {})
                for size, url in logos_data.items():
                    Logo.objects.create(
                        location=location,
                        size=size,
                        url=url
                    )

        self.stdout.write(self.style.SUCCESS('Locations data imported successfully'))
