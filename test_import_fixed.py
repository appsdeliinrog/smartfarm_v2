#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('c:\\Users\\fsociety\\Documents\\agri-open')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from crops.models import PDFUpload, ParsedRecord, PriceObservation
from crops.services import DataImportService
from datetime import date

def test_import():
    print("=== Import Test (Fixed Version) ===")
    
    # Find the February upload
    feb_upload = PDFUpload.objects.filter(file_name__icontains='21st July').first()
    
    if not feb_upload:
        print("No February upload found")
        return
    
    print(f"Upload: {feb_upload.file_name}")
    print(f"Status: {feb_upload.status}")
    print(f"Records imported: {feb_upload.records_imported}")
    
    # Check parsed records
    parsed_records = ParsedRecord.objects.filter(upload=feb_upload)
    print(f"Parsed records: {parsed_records.count()}")
    
    valid_records = parsed_records.filter(is_valid=True)
    print(f"Valid records: {valid_records.count()}")
    
    pending_records = parsed_records.filter(import_action='pending')
    print(f"Pending import: {pending_records.count()}")
    
    # Check if data exists in PriceObservation for Feb 21
    feb_21_data = PriceObservation.objects.filter(observed_date=date(2025, 7, 21))
    print(f"Feb 21 data in PriceObservation: {feb_21_data.count()}")
    
    if pending_records.exists():
        print("\n=== Attempting Import ===")
        import_service = DataImportService()
        
        # Try importing a few records manually
        test_records = pending_records[:5]
        success_count = 0
        
        for record in test_records:
            try:
                import_service.import_single_record(record, 'skip')
                success_count += 1
                print(f"✅ Successfully imported record {record.id}")
            except Exception as e:
                print(f"❌ Failed to import record {record.id}: {str(e)}")
        
        print(f"\n=== Test Results ===")
        print(f"Successfully imported: {success_count}/{test_records.count()}")
        
        # Check if data now exists
        feb_21_data_after = PriceObservation.objects.filter(observed_date=date(2025, 7, 21))
        print(f"Feb 21 data after test import: {feb_21_data_after.count()}")

if __name__ == "__main__":
    test_import()
