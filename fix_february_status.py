#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('c:\\Users\\fsociety\\Documents\\agri-open')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from crops.models import ParsedRecord, PDFUpload, PriceObservation
from datetime import date

def fix_february_status():
    print("=== Fixing February Import Status ===")
    
    # Get the February upload
    feb_upload = PDFUpload.objects.filter(file_name__icontains='21th February').first()
    if not feb_upload:
        print("February upload not found")
        return
        
    print(f"Upload: {feb_upload.file_name}")
    
    # Get all parsed records for this upload
    parsed_records = ParsedRecord.objects.filter(upload=feb_upload, is_valid=True)
    print(f"Total valid parsed records: {parsed_records.count()}")
    
    # Check which ones were actually imported (exist in PriceObservation)
    imported_count = 0
    failed_count = 0
    
    for record in parsed_records:
        # Check if this record exists in PriceObservation
        exists = PriceObservation.objects.filter(
            observed_date=record.date,
            market__name=record.market,
            commodity__name=record.commodity,
            stat=record.stat,
            price=record.price_per_kg
        ).exists()
        
        if exists:
            if record.import_action == 'pending':
                record.import_action = 'imported'
                record.save()
                imported_count += 1
        else:
            if record.import_action == 'pending':
                record.import_action = 'failed'
                record.save()
                failed_count += 1
    
    print(f"Updated {imported_count} records to 'imported' status")
    print(f"Updated {failed_count} records to 'failed' status")
    
    # Show final status
    final_stats = {}
    for status in ['pending', 'imported', 'failed', 'skipped']:
        count = parsed_records.filter(import_action=status).count()
        final_stats[status] = count
        print(f"{status.capitalize()}: {count}")
    
    # Verify with actual PriceObservation data
    feb_data = PriceObservation.objects.filter(observed_date=date(2025, 2, 21))
    print(f"\nActual February data in PriceObservation: {feb_data.count()} records")

if __name__ == "__main__":
    fix_february_status()
