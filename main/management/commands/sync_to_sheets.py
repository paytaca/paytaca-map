import logging
from django.core.management.base import BaseCommand
from django.db import models
from main.models import Merchant
import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)


# Category mapping to numbers as defined by stakeholders
CATEGORY_MAPPING = {
    "Tourism": 0,
    "Clothing": 1,
    "Digital Consulting": 2,
    "Services": 3,
    "Food and Beverages": 4,
    "Home Appliances": 5,
    "Gastronomy": 6,
    "Hobbies": 7,
    "Hygiene and Beauty": 8,
    "Toys and Books": 9,
    "Garden and Gifts": 10,
    "Apparel and Footwear": 11,
    "Transport and Customs": 12,
    "Office Supplies": 13,
    "Computing": 14,
    "Other": 15,
}


class Command(BaseCommand):
    help = "Syncs merchant data to Google Sheets for external stakeholders"

    def get_service_account_credentials(self):
        """Get service account credentials from settings or environment."""
        credentials_info = {
            "type": "service_account",
            "project_id": getattr(settings, "GOOGLE_PROJECT_ID", ""),
            "private_key_id": getattr(settings, "GOOGLE_PRIVATE_KEY_ID", ""),
            "private_key": getattr(settings, "GOOGLE_PRIVATE_KEY", "").replace(
                "\\n", "\n"
            ),
            "client_email": getattr(settings, "GOOGLE_CLIENT_EMAIL", ""),
            "client_id": getattr(settings, "GOOGLE_CLIENT_ID", ""),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": getattr(settings, "GOOGLE_CLIENT_CERT_URL", ""),
            "universe_domain": "googleapis.com",
        }

        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        return Credentials.from_service_account_info(credentials_info, scopes=scopes)

    def get_category_number(self, merchant):
        """Get the category number for a merchant."""
        categories = merchant.categories.all()
        if not categories:
            return 15  # Other

        # Try to match the first category to our mapping
        first_category = categories[0].name
        for key, value in CATEGORY_MAPPING.items():
            if key.lower() in first_category.lower():
                return value

        return 15  # Default to Other if no match

    def get_coordinates(self, merchant):
        """Format coordinates as 'latitude,longitude'."""
        if merchant.latitude is None or merchant.longitude is None:
            return ""
        return f"{merchant.latitude},{merchant.longitude}"

    def get_direction(self, merchant):
        """Combine address fields into Direction."""
        parts = []
        if merchant.street:
            parts.append(merchant.street)
        if merchant.landmark:
            parts.append(merchant.landmark)
        if merchant.location:
            parts.append(merchant.location)

        return ", ".join(parts) if parts else ""

    def get_keywords(self, merchant):
        """Generate keywords from merchant name and categories."""
        keywords = [merchant.name]
        for category in merchant.categories.all():
            keywords.append(category.name)
        return ", ".join(keywords)

    def get_merchants_data(self):
        """Fetch merchant data formatted for external stakeholders."""
        merchants = (
            Merchant.objects.filter(test_shop=False, verified=True, active=True)
            .filter(
                models.Q(last_transaction_date__isnull=False)
                | models.Q(categories__name="Hotels / Resorts by Hiverooms")
            )
            .filter(longitude__isnull=False, latitude__isnull=False)
            .distinct()
        )

        data = []
        for merchant in merchants:
            # Display: 1 if verified and has transactions, 0 otherwise
            display = 1 if merchant.verified and merchant.last_transaction_date else 1

            row = [
                display,  # Display
                "",  # Discount - not in our DB
                merchant.name,  # Business Name
                self.get_category_number(merchant),  # Business Category (number)
                self.get_direction(merchant),  # Direction
                merchant.city or "",  # City
                merchant.state or merchant.province or "",  # State
                merchant.country or "",  # Country
                "",  # Business Number - not in our DB
                "",  # Email - not in our DB
                merchant.website_url or "",  # Website
                self.get_keywords(merchant),  # Key Words
                self.get_coordinates(merchant),  # Coordinates
                2,  # Business Type - default to Local Store (2)
                merchant.logo_url or "",  # Logo
                merchant.last_update.isoformat()
                if merchant.last_update
                else datetime.now().isoformat(),  # Timestamp
            ]
            data.append(row)

        return data

    def sync_to_sheet(self, spreadsheet_id, sheet_name="Sheet1"):
        """Sync merchant data to Google Sheet."""
        try:
            credentials = self.get_service_account_credentials()
            gc = gspread.authorize(credentials)

            # Open spreadsheet
            spreadsheet = gc.open_by_key(spreadsheet_id)

            # Try to get the worksheet, create if it doesn't exist
            try:
                worksheet = spreadsheet.worksheet(sheet_name)
            except gspread.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(
                    title=sheet_name, rows=1000, cols=16
                )

            # Get data before clearing
            data = self.get_merchants_data()

            # Clear existing data rows (starting from row 2, preserving headers in row 1)
            # First, get the current number of rows
            current_rows = worksheet.row_count
            if current_rows > 1:
                # Delete all rows from row 2 onwards
                worksheet.delete_rows(2, current_rows)

            # Resize worksheet to accommodate new data (keep row 1 for headers)
            if data:
                total_rows_needed = len(data) + 1  # +1 for header row
                if total_rows_needed > worksheet.row_count:
                    worksheet.add_rows(total_rows_needed - worksheet.row_count)

            # Insert data starting from row 2
            if data:
                worksheet.insert_rows(data, row=2)

            logger.info(f"Successfully synced {len(data)} merchants to Google Sheet")
            return True

        except Exception as e:
            logger.error(f"Error syncing to Google Sheets: {str(e)}")
            return False

    def handle(self, *args, **options):
        spreadsheet_id = getattr(settings, "GOOGLE_SHEETS_SPREADSHEET_ID", "")

        if not spreadsheet_id:
            logger.error("GOOGLE_SHEETS_SPREADSHEET_ID not configured in settings")
            return

        success = self.sync_to_sheet(spreadsheet_id)

        if success:
            self.stdout.write(
                self.style.SUCCESS("Successfully synced merchants to Google Sheets")
            )
        else:
            self.stdout.write(
                self.style.ERROR("Failed to sync merchants to Google Sheets")
            )
