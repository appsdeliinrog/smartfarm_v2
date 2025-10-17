#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('c:\\Users\\fsociety\\Documents\\agri-open')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from crops.models import Commodity, PriceObservation, ParsedRecord
from collections import Counter

def analyze_commodities():
    print("=== Commodity Analysis ===")
    
    # Get all commodities
    commodities = Commodity.objects.all().order_by('name')
    print(f"Total commodities in database: {commodities.count()}")
    
    print("\n=== All Commodities ===")
    for commodity in commodities:
        # Count how many price observations each commodity has
        price_count = PriceObservation.objects.filter(commodity=commodity).count()
        print(f"- {commodity.name}")
        if commodity.swahili_name:
            print(f"  Swahili: {commodity.swahili_name}")
        print(f"  Category: {commodity.category}")
        print(f"  Unit: {commodity.unit}")
        print(f"  Price observations: {price_count}")
        print()
    
    # Check for potential duplicates or variations
    print("=== Checking for Similar Names ===")
    commodity_names = [c.name.lower() for c in commodities]
    
    # Look for potential variations
    variations = {}
    for commodity in commodities:
        name_lower = commodity.name.lower()
        # Check for common variations
        base_words = name_lower.split()
        for other in commodities:
            if other.id != commodity.id:
                other_lower = other.name.lower()
                # Check if they share common words
                other_words = other_lower.split()
                common_words = set(base_words) & set(other_words)
                if common_words and len(common_words) >= 1:
                    key = tuple(sorted(common_words))
                    if key not in variations:
                        variations[key] = []
                    variations[key].append(commodity.name)
    
    for common_words, names in variations.items():
        if len(set(names)) > 1:  # More than one unique name
            print(f"Similar commodities with '{' '.join(common_words)}':")
            for name in set(names):
                print(f"  - {name}")
            print()
    
    # Check commodity usage in parsed records
    print("=== Commodity Usage in ParsedRecords ===")
    parsed_commodities = ParsedRecord.objects.values_list('commodity', flat=True)
    commodity_usage = Counter(parsed_commodities)
    
    print("Top 10 most common commodities in parsed data:")
    for commodity_name, count in commodity_usage.most_common(10):
        print(f"  {commodity_name}: {count} records")
    
    # Check for commodities in parsed records that don't exist in Commodity table
    print("\n=== Missing Commodities ===")
    unique_parsed_commodities = set(parsed_commodities)
    existing_commodity_names = set(c.name for c in commodities)
    missing_commodities = unique_parsed_commodities - existing_commodity_names
    
    if missing_commodities:
        print("Commodities in parsed data but not in Commodity table:")
        for missing in sorted(missing_commodities):
            count = commodity_usage[missing]
            print(f"  - {missing}: {count} records")
    else:
        print("All parsed commodities exist in Commodity table ✓")
    
    # Check February data specifically
    print("\n=== February 21st Commodities ===")
    from datetime import date
    feb_commodities = PriceObservation.objects.filter(
        observed_date=date(2025, 2, 21)
    ).values_list('commodity__name', flat=True)
    
    feb_commodity_counts = Counter(feb_commodities)
    print("Commodities in February 21st data:")
    for commodity_name, count in feb_commodity_counts.most_common():
        print(f"  - {commodity_name}: {count} price points")

if __name__ == "__main__":
    analyze_commodities()
