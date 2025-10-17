#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Setup Django
django.setup()

from crops.models import PDFUpload, ParsedRecord, PriceObservation

def debug_import_issue():
    print("=== DEBUG IMPORT ISSUE ===")
    
    # Find the February upload
    feb_uploads = PDFUpload.objects.filter(file_name__contains='21th February')
    print(f"February uploads found: {feb_uploads.count()}")
    
    for upload in feb_uploads:
        print(f"\nUpload: {upload.file_name}")
        print(f"Status: {upload.status}")
        print(f"Records imported: {upload.records_imported}")
        print(f"Records skipped: {upload.records_skipped}")
        print(f"Import errors: {upload.import_errors}")
        
        # Check parsed records
        parsed_records = upload.parsed_records.all()
        print(f"Parsed records: {parsed_records.count()}")
        print(f"Valid records: {parsed_records.filter(is_valid=True).count()}")
        print(f"Pending import: {parsed_records.filter(import_action='pending').count()}")
        
        # Check if any were actually imported
        feb_21_data = PriceObservation.objects.filter(observed_date='2025-02-21')
        print(f"Feb 21 data in PriceObservation: {feb_21_data.count()}")
        
        # Check import actions
        import_actions = parsed_records.values_list('import_action', flat=True).distinct()
        print(f"Import actions: {list(import_actions)}")

if __name__ == "__main__":
    debug_import_issue()
