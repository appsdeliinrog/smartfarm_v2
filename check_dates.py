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
from datetime import date

def check_data():
    print("=== Checking February vs July Data ===")
    
    # Check for uploads containing 21
    uploads_21 = PDFUpload.objects.filter(file_name__icontains='21')
    print(f"Uploads containing '21': {uploads_21.count()}")
    
    for upload in uploads_21:
        print(f"- {upload.file_name}")
        print(f"  Status: {upload.status}")
        print(f"  Extracted date: {upload.extracted_date}")
        print(f"  Records imported: {upload.records_imported}")
        print()
    
    # Check actual data in PriceObservation
    print("=== Checking PriceObservation Data ===")
    
    # February 21
    feb_21_data = PriceObservation.objects.filter(observed_date=date(2025, 2, 21))
    print(f"February 21, 2025: {feb_21_data.count()} records")
    
    # July 21  
    july_21_data = PriceObservation.objects.filter(observed_date=date(2025, 7, 21))
    print(f"July 21, 2025: {july_21_data.count()} records")
    
    # Show some sample dates
    print("\n=== Recent Dates in Database ===")
    recent_dates = PriceObservation.objects.values_list('observed_date', flat=True).distinct().order_by('-observed_date')[:10]
    for d in recent_dates:
        count = PriceObservation.objects.filter(observed_date=d).count()
        print(f"{d}: {count} records")

if __name__ == "__main__":
    check_data()
