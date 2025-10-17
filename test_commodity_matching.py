"""
Test script for the smart commodity matching service
Run this to verify the matching logic works correctly
"""
import os
import sys
import django

# Setup Django
sys.path.append(r'c:\Users\fsociety\Documents\agri-open')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from crops.commodity_matching import CommodityMatchingService

def test_commodity_matching():
    """Test various commodity name variations"""
    
    test_cases = [
        # Known variations that should match
        "Beans (Maharage)",
        "Beans",
        "Maharage", 
        "BEANS",
        "beans",
        "Rice (Mchele)",
        "Rice",
        "Mchele",
        "Maize (Mahindi)",
        "Maize",
        "Mahindi",
        "Corn",
        "Wheat Grain (Ngano)",
        "Wheat",
        "Wheat Grain",
        "Ngano",
        "Sorghum (Mtama)",
        "Sorghum",
        "Mtama",
        "Finger Millet (Ulezi)",
        "Finger Millet",
        "Ulezi",
        "Bulrush Millet (Uwele)",
        "Bulrush Millet",
        "Uwele",
        "Irish Potatoes (Viazi Mviringo)",
        "Irish Potatoes",
        "Potatoes",
        "Viazi Mviringo",
        
        # Edge cases
        "",
        "Unknown Crop",
        "Sweet Potatoes",
        "Tomatoes",
        "  Beans  ",  # Extra whitespace
        "beans (maharage)",  # Lowercase
        "RICE (MCHELE)",  # Uppercase
    ]
    
    print("🧪 TESTING COMMODITY MATCHING SERVICE")
    print("="*60)
    
    for test_name in test_cases:
        result = CommodityMatchingService.normalize_commodity_name(test_name)
        
        status = "✅ MATCHED" if result['matched'] else "⚠️  NEW"
        swahili_part = f" / {result['swahili_name']}" if result['swahili_name'] else ""
        
        print(f"{status} '{test_name}'")
        print(f"   → {result['name']}{swahili_part}")
        
        if not result['matched'] and test_name.strip():
            print("   ⚠️  Would create new commodity")
        print()
    
    # Test bulk analysis
    print("\n🔍 TESTING BULK ANALYSIS")
    print("="*60)
    
    test_records = [
        {'commodity': 'Beans (Maharage)'},
        {'commodity': 'Beans'},
        {'commodity': 'Rice (Mchele)'},
        {'commodity': 'Unknown Crop'},
        {'commodity': 'Beans (Maharage)'},  # Duplicate
    ]
    
    # Mock parsed records for testing
    class MockRecord:
        def __init__(self, commodity):
            self.commodity = commodity
    
    mock_records = [MockRecord(r['commodity']) for r in test_records]
    analysis = CommodityMatchingService.analyze_parsed_commodities(mock_records)
    
    for raw_name, info in analysis.items():
        status = "✅ MATCHED" if info['matched'] else "⚠️  NEW"
        swahili_part = f" / {info['suggested_swahili']}" if info['suggested_swahili'] else ""
        
        print(f"{status} '{raw_name}' ({info['count']} records)")
        print(f"   → {info['suggested_name']}{swahili_part}")
        print()

if __name__ == "__main__":
    test_commodity_matching()
