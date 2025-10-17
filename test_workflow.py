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

def test_complete_workflow():
    print("=== Complete Import Workflow Test ===")
    
    # Get an upload that hasn't been imported yet (if any)
    pending_uploads = PDFUpload.objects.filter(status__in=['uploaded', 'parsed']).exclude(file_name__icontains='21st July')
    
    if pending_uploads.exists():
        upload = pending_uploads.first()
        print(f"Testing with: {upload.file_name}")
        
        # Check parsed records
        parsed_records = ParsedRecord.objects.filter(upload=upload, is_valid=True, import_action='pending')
        print(f"Pending records to import: {parsed_records.count()}")
        
        if parsed_records.exists():
            # Test the import service
            import_service = DataImportService()
            results = import_service.import_parsed_records(upload.id, import_mode='skip')
            
            print(f"Import results: {results}")
            
            # Check if upload status was updated
            upload.refresh_from_db()
            print(f"Upload status after import: {upload.status}")
            print(f"Records imported: {upload.records_imported}")
        else:
            print("No pending records found for this upload")
    else:
        print("No pending uploads found to test with")
    
    print("\n=== Testing February Data ===")
    feb_upload = PDFUpload.objects.filter(file_name__icontains='21st July').first()
    print(f"February upload status: {feb_upload.status}")
    print(f"February records imported: {feb_upload.records_imported}")
    
    # Double-check the data exists
    feb_data = PriceObservation.objects.filter(observed_date=date(2025, 7, 21))
    print(f"February data in database: {feb_data.count()}")

if __name__ == "__main__":
    test_complete_workflow()
