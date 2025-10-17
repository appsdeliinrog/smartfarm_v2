#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('c:\\Users\\fsociety\\Documents\\agri-open')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from crops.models import Commodity, PriceObservation
from django.db import transaction

def consolidate_commodities():
    """
    Consolidate duplicate commodities by merging them into unified records
    """
    print("=== Commodity Consolidation Script ===")
    
    # Define the mapping from duplicates to canonical names
    commodity_mappings = {
        # Format: "duplicate_name": {"canonical_name": "main_name", "swahili_name": "swahili"}
        "Beans (Maharage)": {"canonical_name": "Beans", "swahili_name": "Maharage"},
        "Bulrush Millet (Uwele)": {"canonical_name": "Bulrush Millet", "swahili_name": "Uwele"},
        "Finger Millet (Ulezi)": {"canonical_name": "Finger Millet", "swahili_name": "Ulezi"},
        "Irish Potatoes (Viazi Mviringo)": {"canonical_name": "Irish Potatoes", "swahili_name": "Viazi Mviringo"},
        "Maize (Mahindi)": {"canonical_name": "Maize", "swahili_name": "Mahindi"},
        "Rice (Mchele)": {"canonical_name": "Rice", "swahili_name": "Mchele"},
        "Sorghum (Mtama)": {"canonical_name": "Sorghum", "swahili_name": "Mtama"},
        "Wheat Grain (Ngano)": {"canonical_name": "Wheat Grain", "swahili_name": "Ngano"},
    }
    
    with transaction.atomic():
        for duplicate_name, mapping in commodity_mappings.items():
            canonical_name = mapping["canonical_name"]
            swahili_name = mapping["swahili_name"]
            
            try:
                # Get the duplicate commodity
                duplicate_commodity = Commodity.objects.get(name=duplicate_name)
                canonical_commodity = Commodity.objects.get(name=canonical_name)
                
                print(f"\nProcessing: {duplicate_name} -> {canonical_name}")
                
                # Update the canonical commodity with Swahili name if not already set
                if not canonical_commodity.swahili_name:
                    canonical_commodity.swahili_name = swahili_name
                    canonical_commodity.save()
                    print(f"  ✓ Updated {canonical_name} swahili_name to '{swahili_name}'")
                
                # Move all price observations from duplicate to canonical
                price_observations = PriceObservation.objects.filter(commodity=duplicate_commodity)
                moved_count = price_observations.count()
                
                price_observations.update(commodity=canonical_commodity)
                print(f"  ✓ Moved {moved_count} price observations")
                
                # Delete the duplicate commodity
                duplicate_commodity.delete()
                print(f"  ✓ Deleted duplicate commodity '{duplicate_name}'")
                
            except Commodity.DoesNotExist as e:
                print(f"  ⚠️ Commodity not found: {e}")
            except Exception as e:
                print(f"  ❌ Error processing {duplicate_name}: {e}")
    
    print("\n=== Final Commodity Status ===")
    commodities = Commodity.objects.all().order_by('name')
    for commodity in commodities:
        price_count = PriceObservation.objects.filter(commodity=commodity).count()
        swahili_display = f" ({commodity.swahili_name})" if commodity.swahili_name else ""
        print(f"- {commodity.name}{swahili_display}: {price_count} price observations")

if __name__ == "__main__":
    consolidate_commodities()
