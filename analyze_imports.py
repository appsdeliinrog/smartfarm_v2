#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('c:\\Users\\fsociety\\Documents\\agri-open')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from crops.models import ParsedRecord, PDFUpload, Market
from collections import Counter

def analyze_import_issues():
    print("=== Import Status Analysis ===")
    
    # Check the February upload
    feb_upload = PDFUpload.objects.filter(file_name__icontains='21th February').first()
    if not feb_upload:
        print("February upload not found")
        return
        
    print(f"Upload: {feb_upload.file_name}")
    print(f"Status: {feb_upload.status}")
    print(f"Records imported: {feb_upload.records_imported}")
    
    # Check parsed records status
    parsed_records = ParsedRecord.objects.filter(upload=feb_upload)
    print(f"\n=== ParsedRecord Status ===")
    print(f"Total parsed records: {parsed_records.count()}")
    print(f"Valid records: {parsed_records.filter(is_valid=True).count()}")
    print(f"Pending import: {parsed_records.filter(import_action='pending').count()}")
    print(f"Imported records: {parsed_records.filter(import_action='imported').count()}")
    print(f"Failed records: {parsed_records.filter(import_action='failed').count()}")
    
    # Check duplicate markets issue
    print(f"\n=== Duplicate Markets Analysis ===")
    markets = Market.objects.values_list('name', flat=True)
    market_counts = Counter(markets)
    duplicates = {name: count for name, count in market_counts.items() if count > 1}
    
    print(f"Total unique market names: {len(set(markets))}")
    print(f"Markets with duplicates: {len(duplicates)}")
    
    for market_name, count in duplicates.items():
        print(f"\n{market_name}: {count} entries")
        markets_with_regions = Market.objects.filter(name=market_name).values_list('region__name', flat=True)
        regions = list(markets_with_regions)
        print(f"  Regions: {', '.join(regions)}")
        
        # Check how many failed records have this market name
        failed_with_this_market = parsed_records.filter(
            import_action='pending', 
            market=market_name
        ).count()
        if failed_with_this_market > 0:
            print(f"  Failed records: {failed_with_this_market}")

if __name__ == "__main__":
    analyze_import_issues()
